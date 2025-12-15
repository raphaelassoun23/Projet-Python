import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset="timestamp").copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    cols_to_interpolate = [
        "BTC_price","BTC_volume","BTC_open","BTC_high","BTC_low",
        "ETH_price","ETH_volume","ETH_open","ETH_high","ETH_low",
    ]
    df[cols_to_interpolate] = df[cols_to_interpolate].interpolate(method="linear")
    return df

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("timestamp").copy()

    for col in ["BTC", "ETH", "SP500", "NASDAQ"]:
        df[f"{col}_return_daily"] = np.log(df[f"{col}_price"] / df[f"{col}_price"].shift(1))

        if col in ["BTC", "ETH"]:
            df[f"{col}_volatility_7d"] = df[f"{col}_return_daily"].rolling(window=7).std()
            df[f"{col}_volatility_30d"] = df[f"{col}_return_daily"].rolling(window=30).std()
            df[f"{col}_moving_avg_7d"] = df[f"{col}_price"].rolling(window=7).mean()
            df[f"{col}_moving_avg_30d"] = df[f"{col}_price"].rolling(window=30).mean()
            df[f"{col}_range_daily"] = df[f"{col}_high"] - df[f"{col}_low"]
            df[f"{col}_volume_change"] = df[f"{col}_volume"].pct_change()

    # comme le notebook
    return df.dropna().reset_index(drop=True)

def build_final_dataset(df: pd.DataFrame) -> pd.DataFrame:
    return add_features(clean_data(df))
