import pandas as pd
import yfinance as yf
import os
import time
import requests

def get_data_yf(ticker: str, name: str) -> pd.DataFrame:
    df = yf.download(ticker, period="max").reset_index()
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]

    df = df.rename(columns={
        "Date": "timestamp",
        "Open": f"{name}_open",
        "High": f"{name}_high",
        "Low": f"{name}_low",
        "Close": f"{name}_price",
        "Volume": f"{name}_volume",
    })

    # Certains tickers (ex: ^TNX, ^IRX) peuvent avoir Volume=NaN → on garde quand même la colonne
    cols = ["timestamp", f"{name}_price", f"{name}_open", f"{name}_high", f"{name}_low"]
    if f"{name}_volume" in df.columns:
        cols.append(f"{name}_volume")

    return df[cols]

ALPHA_BASE = "https://www.alphavantage.co/query"

def fetch_alpha_vantage_daily(symbol: str, name: str, api_key: str | None = None, adjusted: bool = True) -> pd.DataFrame:
    api_key = api_key or os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        raise ValueError("ALPHAVANTAGE_API_KEY manquant (env var ou param).")

    func = "TIME_SERIES_DAILY_ADJUSTED" if adjusted else "TIME_SERIES_DAILY"
    params = {"function": func, "symbol": symbol, "outputsize": "full", "apikey": api_key}

    r = requests.get(ALPHA_BASE, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()

    # messages d'erreur AV fréquents (rate limit)
    if "Note" in data:
        raise RuntimeError(f"Alpha Vantage rate limit: {data['Note']}")
    if "Error Message" in data:
        raise RuntimeError(f"Alpha Vantage error: {data['Error Message']}")

    key = "Time Series (Daily)"
    if key not in data:
        raise RuntimeError(f"Réponse inattendue Alpha Vantage: keys={list(data.keys())}")

    ts = pd.DataFrame.from_dict(data[key], orient="index")
    ts.index = pd.to_datetime(ts.index)
    ts = ts.sort_index()

    # Colonnes AV: '1. open', '2. high', '3. low', '4. close', '6. volume'
    out = pd.DataFrame({
        "timestamp": ts.index,
        f"{name}_open":  pd.to_numeric(ts["1. open"], errors="coerce"),
        f"{name}_high":  pd.to_numeric(ts["2. high"], errors="coerce"),
        f"{name}_low":   pd.to_numeric(ts["3. low"], errors="coerce"),
        f"{name}_price": pd.to_numeric(ts["4. close"], errors="coerce"),
        f"{name}_volume": pd.to_numeric(ts["6. volume"], errors="coerce") if "6. volume" in ts.columns else pd.NA,
    }).dropna(subset=[f"{name}_price"])

    return out


def fetch_dataset(tickers: dict[str, str]) -> pd.DataFrame:
    dfs = []
    for name, ticker in tickers.items():
        dfs.append(get_data_yf(ticker, name))

    # merge successif sur timestamp
    out = dfs[0]
    for d in dfs[1:]:
        out = out.merge(d, on="timestamp", how="inner")

    return out

def fetch_dataset_with_alpha(tickers: dict[str, str]) -> pd.DataFrame:
    dfs = []
    for name, symbol in tickers.items():
        dfs.append(fetch_alpha_vantage_daily(symbol=symbol, name=name))
        time.sleep(15)  # Alpha Vantage gratuit: évite rate limit (à ajuster)
    out = dfs[0]
    for d in dfs[1:]:
        out = out.merge(d, on="timestamp", how="inner")
    return out

