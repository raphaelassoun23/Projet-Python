import pandas as pd
import yfinance as yf

# fetch.py
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

    # Certains tickers (ex: ^TNX, ^IRX) peuvent avoir Volume=NaN → on garde quand même la colonne
    cols = ["timestamp", f"{name}_price", f"{name}_open", f"{name}_high", f"{name}_low"]
    if f"{name}_volume" in df.columns:
        cols.append(f"{name}_volume")

    return df[cols]

def fetch_dataset(tickers: dict[str, str]) -> pd.DataFrame:
    dfs = []
    for name, ticker in tickers.items():
        dfs.append(get_data_yf(ticker, name))

    # merge successif sur timestamp
    out = dfs[0]
    for d in dfs[1:]:
        out = out.merge(d, on="timestamp", how="inner")

    return out
