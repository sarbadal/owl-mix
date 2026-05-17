import pandas as pd
from typing import TypedDict, NotRequired


class TimeConfig(TypedDict):
    start_date: str
    end_date: str
    frequency: NotRequired[str]
    

class TimeSeriesBuilder:
    """
    Builds a time series DataFrame based on the specified time configuration.
    The time configuration can be provided under either 'dataset' or 'time' keys in the config dictionary.
    Args:
        config (dict): Configuration dictionary containing time settings.
    """
    def __init__(self, config: dict):
        self.config = config
        self.time_config: TimeConfig = self._extract_time_config()

    def _extract_time_config(self) -> TimeConfig:
        if "dataset" in self.config:
            return self.config["dataset"]
        if "time" in self.config:
            return self.config["time"]
        raise ValueError("Missing time configuration: expected 'dataset' or 'time'")

    def build(self) -> pd.DataFrame:
        """Builds a time series DataFrame based on the specified time configuration."""
        start_date = self.time_config["start_date"]
        end_date = self.time_config["end_date"]
        freq = self.time_config.get("frequency", "weekly")
        pandas_freq = self._map_frequency(freq)
        date_range = pd.date_range(start=start_date, end=end_date, freq=pandas_freq)
        df = pd.DataFrame({"date": date_range})
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["week"] = df["date"].dt.isocalendar().week.astype(int)
        return df

    @staticmethod
    def _map_frequency(freq: str) -> str:
        mapping = {
            "daily": "D",
            "weekly": "W",
            "monthly": "M"
        }
        if freq not in mapping:
            raise ValueError(
                f"Invalid frequency '{freq}'. Choose from daily, weekly, monthly."
            )
        return mapping[freq]