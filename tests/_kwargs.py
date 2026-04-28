from typing import TypedDict, Unpack, Union
import pandas as pd


class Columns(TypedDict):
    target: str
    date: str
    features: list[str]


def process(data: pd.DataFrame, **columns: Unpack[Columns]) -> pd.DataFrame:
    df = pd.DataFrame()
    target = columns["target"]
    date = columns["date"]
    features = columns["features"]

    df[target] = data[target].astype("int")
    df[date] = pd.to_datetime(data[date])

    for feature in features:
        df[feature] = data[feature].astype("int")

    return df


def main():
     df = pd.DataFrame(
         {
             "target": [11, 34, 54, 98,23],
             "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
             "impressions": [11, 34, 54, 98, 23],
             "clicks": [11, 34, 54, 98, 23],
             "grp": [11, 34, 54, 98, 23],
         }
     )

     processed_df = process(
         df,
         target="target",
         date="date",
         features=["impressions", "clicks", "grp"],
     )

     print(processed_df.head())

     print(df)

if __name__ == "__main__":
    main()