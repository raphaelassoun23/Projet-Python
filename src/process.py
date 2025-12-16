import pandas as pd
import numpy as np

# process.py
import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset="timestamp").copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    cols_to_interpolate = [
        "BTC_price","BTC_volume","BTC_open","BTC_high","BTC_low",
        "ETH_price","ETH_volume","ETH_open","ETH_high","ETH_low",
    ]
    existing = [c for c in cols_to_interpolate if c in df.columns]
    if existing:
        df[existing] = df[existing].interpolate(method="linear")
    return df

def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("timestamp").copy()

    # détecte automatiquement les actifs disponibles
    assets = sorted({c.replace("_price", "") for c in df.columns if c.endswith("_price")})

    rate_assets = {"US10Y", "US3M", "US30Y"}  # yields: on préfère Δy plutôt que log-return

    for col in assets:
        if f"{col}_price" not in df.columns:
            continue

        if col in rate_assets:
            # Variation quotidienne du taux (attention: ^TNX et ^TYX sont souvent *10, ^IRX souvent *100)
            df[f"{col}_return_daily"] = df[f"{col}_price"].diff()
        else:
            df[f"{col}_return_daily"] = np.log(df[f"{col}_price"] / df[f"{col}_price"].shift(1))

        # On ne calcule les features "crypto" que si colonnes existent
        if col in ["BTC", "ETH"]:
            df[f"{col}_volatility_7d"] = df[f"{col}_return_daily"].rolling(window=7).std()
            df[f"{col}_volatility_30d"] = df[f"{col}_return_daily"].rolling(window=30).std()
            df[f"{col}_moving_avg_7d"] = df[f"{col}_price"].rolling(window=7).mean()
            df[f"{col}_moving_avg_30d"] = df[f"{col}_price"].rolling(window=30).mean()

            if f"{col}_high" in df.columns and f"{col}_low" in df.columns:
                df[f"{col}_range_daily"] = df[f"{col}_high"] - df[f"{col}_low"]

            if f"{col}_volume" in df.columns:
                df[f"{col}_volume_change"] = df[f"{col}_volume"].pct_change()

    return df.dropna().reset_index(drop=True)

def build_final_dataset(df: pd.DataFrame) -> pd.DataFrame:
    return add_features(clean_data(df))

