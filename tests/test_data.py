"""Check the shipped excerpt independently of the original MAT files."""

import pandas as pd

from v1_pandas_practice import load_traces


def test_bundled_data_has_complete_v1_segments() -> None:
    traces = load_traces()
    assert list(traces.columns) == [
        "cell_id",
        "frame",
        "time_s",
        "dff",
        "spike_count",
    ]
    assert len(traces) == 14_400
    assert not traces.isna().any().any()
    assert set(traces.cell_id) == {"cell1", "cell4C", "cell5C", "cell7C"}
    assert traces.groupby("cell_id").size().eq(3_600).all()
    assert traces.groupby("cell_id").frame.min().eq(0).all()
    assert traces.groupby("cell_id").frame.max().eq(3_599).all()
    assert (
        traces.groupby("cell_id")
        .time_s.apply(lambda t: t.is_monotonic_increasing)
        .all()
    )
    assert pd.api.types.is_integer_dtype(traces.spike_count)
    assert traces.spike_count.ge(0).all()
    assert traces.spike_count.sum() == 215
