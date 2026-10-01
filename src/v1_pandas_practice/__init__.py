"""Small, self-contained V1 trace dataset for pandas practice."""

from importlib.resources import files

import pandas as pd

DATA_FILE = "v1_calcium_traces.csv"


def load_traces() -> pd.DataFrame:
    """Load the bundled frame-level V1 calcium and spike observations."""
    resource = files("v1_pandas_practice").joinpath("data", DATA_FILE)
    with resource.open("r", encoding="utf-8") as stream:
        return pd.read_csv(stream)
