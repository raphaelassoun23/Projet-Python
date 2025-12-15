import pandas as pd
import yfinance as yf

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

    return df[[
        "timestamp",
        f"{name}_price", f"{name}_volume",
        f"{name}_open", f"{name}_high", f"{name}_low",
    ]]

def fetch_dataset(tickers: dict[str, str]) -> pd.DataFrame:
    btc_df = get_data_yf(tickers["BTC"], "BTC")
    eth_df = get_data_yf(tickers["ETH"], "ETH")
    sp500_df = get_data_yf(tickers["SP500"], "SP500")
    nasdaq_df = get_data_yf(tickers["NASDAQ"], "NASDAQ")

    df = pd.merge(btc_df, eth_df, on="timestamp", how="inner")
    df = df.merge(sp500_df, on="timestamp", how="inner")
    df = df.merge(nasdaq_df, on="timestamp", how="inner")
    return df
