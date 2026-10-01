"""Rebuild the bundled CSV from the upstream CascadeTorch V1 recordings."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
from scipy.io import loadmat

FILES = {
    "cell1": "CAttached_Chen2013_GC6f_cell1_mini.mat",
    "cell4C": "CAttached_Chen2013_GC6f_cell4C_mini.mat",
    "cell5C": "CAttached_Chen2013_GC6f_cell5C_mini.mat",
    "cell7C": "CAttached_Chen2013_GC6f_cell7C_full_mini.mat",
}
DATASET = "DS09-GCaMP6f-m-V1"
FRAME_LIMIT = 3_600
FIELDS = ("cell_id", "frame", "time_s", "dff", "spike_count")


def export(source_dir: Path, output: Path) -> None:
    """Write the first 3,600 frames of segment zero for four V1 cells."""
    source_dir = source_dir / DATASET
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(FIELDS)
        for cell_id, filename in FILES.items():
            segments = np.atleast_1d(
                loadmat(source_dir / filename, squeeze_me=True, struct_as_record=False)[
                    "CAttached"
                ]
            )
            segment = segments[0]
            times = np.asarray(segment.fluo_time[:FRAME_LIMIT], dtype=float)
            dff = np.asarray(segment.fluo_mean[:FRAME_LIMIT], dtype=float)
            events_s = np.asarray(segment.events_AP, dtype=float) / 10_000.0
            if len(times) != FRAME_LIMIT or len(dff) != FRAME_LIMIT:
                raise ValueError(f"{filename} has too few frames")
            if not (np.all(np.isfinite(times)) and np.all(np.isfinite(dff))):
                raise ValueError(f"{filename} contains non-finite trace values")
            if np.any(np.diff(times) <= 0):
                raise ValueError(f"{filename} has non-increasing frame times")
            edges = np.empty(FRAME_LIMIT + 1, dtype=float)
            edges[1:-1] = (times[:-1] + times[1:]) / 2
            edges[0] = times[0] - (times[1] - times[0]) / 2
            edges[-1] = times[-1] + (times[-1] - times[-2]) / 2
            spike_counts, _ = np.histogram(events_s, bins=edges)
            for frame, (time_s, value, spike_count) in enumerate(
                zip(times, dff, spike_counts, strict=True)
            ):
                writer.writerow(
                    (cell_id, frame, f"{time_s:.9f}", f"{value:.9f}", spike_count)
                )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("src/v1_pandas_practice/data/v1_calcium_traces.csv"),
    )
    args = parser.parse_args()
    export(args.source_dir, args.output)


if __name__ == "__main__":
    main()
