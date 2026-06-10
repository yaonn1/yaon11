from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {"timestamp", "close"}


def load_price_data(path: str | Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"Price data is missing required columns: {missing_text}")

    data = data.copy()
    data["timestamp"] = pd.to_datetime(data["timestamp"], utc=True)
    data = data.sort_values("timestamp").reset_index(drop=True)
    data["close"] = data["close"].astype(float)
    return data
