"""Reference results and feedback for the six pandas quests."""

from __future__ import annotations

import importlib.util
from collections.abc import Callable
from pathlib import Path

import pandas as pd

from v1_pandas_practice import load_traces

Answer = pd.DataFrame | pd.Series
Quest = tuple[str, str, Callable[[pd.DataFrame], Answer]]


def _spikes_by_cell(df: pd.DataFrame) -> pd.Series:
    return df.groupby("cell_id")["spike_count"].sum().sort_values(ascending=False)


def _high_fluorescence_frames(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df["dff"] > 0.3, ["cell_id", "time_s", "dff"]].reset_index(drop=True)


def _fluorescence_by_cell(df: pd.DataFrame) -> pd.Series:
    return df.groupby("cell_id")["dff"].mean().sort_index()


def _spikes_by_ten_seconds(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.assign(bin_start_s=(df["time_s"] // 10).astype(int) * 10)
        .groupby(["cell_id", "bin_start_s"], as_index=False)["spike_count"]
        .sum()
        .sort_values(["cell_id", "bin_start_s"])
        .reset_index(drop=True)
    )


def _rolling_fluorescence(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(
        rolling_dff=df.groupby("cell_id")["dff"].transform(
            lambda values: values.rolling(30, min_periods=1).mean()
        )
    )


def _fluorescence_on_spike_frames(df: pd.DataFrame) -> pd.Series:
    return df.assign(has_spike=df["spike_count"] > 0).groupby("has_spike")["dff"].mean()


QUESTS: dict[str, Quest] = {
    "spikes_by_cell": (
        "The spike leaderboard",
        "groupby('cell_id'), sum(), then sort_values()",
        _spikes_by_cell,
    ),
    "high_fluorescence_frames": (
        "The glowing frames",
        "Use .loc with dff > 0.3, select three columns, reset_index()",
        _high_fluorescence_frames,
    ),
    "fluorescence_by_cell": (
        "The average glow",
        "groupby('cell_id')['dff'].mean().sort_index()",
        _fluorescence_by_cell,
    ),
    "spikes_by_ten_seconds": (
        "The ten-second race",
        "Make bin_start_s with time_s // 10, then group and sum",
        _spikes_by_ten_seconds,
    ),
    "rolling_fluorescence": (
        "Smooth the signal",
        "groupby('cell_id')['dff'].transform() with rolling(30, min_periods=1)",
        _rolling_fluorescence,
    ),
    "fluorescence_on_spike_frames": (
        "Do spikes glow?",
        "Create has_spike = spike_count > 0, then group and mean",
        _fluorescence_on_spike_frames,
    ),
}


def check_answers(answer_file: Path, selected: list[str] | None = None) -> bool:
    """Evaluate completed quest functions and print useful feedback."""
    unknown = set(selected or ()) - QUESTS.keys()
    if unknown:
        raise ValueError(f"Unknown quests: {', '.join(sorted(unknown))}")
    spec = importlib.util.spec_from_file_location("practice", answer_file)
    if spec is None or spec.loader is None:
        raise ValueError(f"Cannot load {answer_file}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    traces = load_traces()
    passed = 0
    names = selected or list(QUESTS)
    for name in names:
        title, hint, reference = QUESTS[name]
        try:
            answer = getattr(module, name)(traces.copy())
            expected = reference(traces.copy())
            if isinstance(expected, pd.Series):
                pd.testing.assert_series_equal(answer, expected, check_dtype=False)
            else:
                pd.testing.assert_frame_equal(answer, expected, check_dtype=False)
        except Exception as error:
            detail = str(error).splitlines()[0] if str(error) else type(error).__name__
            print(f"○ {title}: {detail}\n  Hint: {hint}")
        else:
            passed += 1
            print(f"★ {title}: complete")
    print(f"\n{passed}/{len(names)} quests complete")
    return passed == len(names)
