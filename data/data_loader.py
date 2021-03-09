import pandas as pd
from pathlib import Path

pandas_data_args = {"sep": "\t",
                    "names": ["altitude", "meters", "temp", "RH", "speed", "direction"],
                    "header": 0}


def get_site_1_data() -> pd.DataFrame:
    data = pd.read_csv(get_data_dir() / "Site1BalloonData.txt", **pandas_data_args)
    return data


def get_site_2_data() -> pd.DataFrame:
    data = pd.read_csv(get_data_dir() / "Site2BalloonData.txt", **pandas_data_args)
    return data


def get_data_dir() -> Path:
    return get_project_root() / "data"


def get_project_root() -> Path:
    return Path(__file__).parent.parent

# print(get_site_1_data())
# print(get_site_2_data())
