import pandas as pd
from matplotlib import pyplot as plt

def _ensure_datetime(df: pd.DataFrame) -> pd.DataFrame:
    if "timestamp" not in df.columns:
        raise KeyError("Colonne 'timestamp' manquante.")
    out = df.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"])
    return out.sort_values("timestamp")

def print_correlations(df: pd.DataFrame) -> None:
    for target in ["BTC_return_daily", "ETH_return_daily"]:
        cols = [target, "SP500_return_daily", "NASDAQ_return_daily"]
        print(df[cols].corr(), end="\n\n")

    print(df[["ETH_return_daily", "BTC_return_daily"]].corr(), end="\n\n")
    
def plot_btc_sp500(df: pd.DataFrame, window: int = 90) -> None:
    df = _ensure_datetime(df)
    required = ["BTC_return_daily", "SP500_return_daily"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Colonnes manquantes: {missing}")

    rolling_corr = df["BTC_return_daily"].rolling(window=window).corr(df["SP500_return_daily"])

    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], rolling_corr, label="BTC vs SP500")
    plt.axhline(0, linestyle="--")
    plt.xlabel("Date")
    plt.ylabel(f"Rolling {window}-day Correlation")
    plt.title(f"Évolution de la corrélation BTC / S&P 500 ({window} jours)")
    plt.legend()
    plt.show()


def plot_btc_nasdaq(df: pd.DataFrame, window: int = 90) -> None:
    df = _ensure_datetime(df)
    required = ["BTC_return_daily", "NASDAQ_return_daily"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Colonnes manquantes: {missing}")

    rolling_corr = df["BTC_return_daily"].rolling(window=window).corr(df["NASDAQ_return_daily"])

    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], rolling_corr, label="BTC vs NASDAQ")
    plt.axhline(0, linestyle="--")
    plt.xlabel("Date")
    plt.ylabel(f"Rolling {window}-day Correlation")
    plt.title(f"Évolution de la corrélation BTC / NASDAQ ({window} jours)")
    plt.legend()
    plt.show()


def plot_sp500_nasdaq(df: pd.DataFrame, window: int = 90) -> None:
    df = _ensure_datetime(df)
    required = ["SP500_return_daily", "NASDAQ_return_daily"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Colonnes manquantes: {missing}")

    rolling_corr = df["SP500_return_daily"].rolling(window=window).corr(df["NASDAQ_return_daily"])

    plt.figure(figsize=(12, 6))
    plt.plot(df["timestamp"], rolling_corr, label="SP500 vs NASDAQ")
    plt.axhline(0, linestyle="--")
    plt.xlabel("Date")
    plt.ylabel(f"Rolling {window}-day Correlation")
    plt.title(f"Évolution de la corrélation S&P 500 / NASDAQ ({window} jours)")
    plt.legend()
    plt.show()


def plot_event_window(df: pd.DataFrame, event_date: str, window_days: int = 15, rolling_days: int = 10) -> None:
    event_date = pd.to_datetime(event_date)
    start_date = event_date - pd.Timedelta(days=window_days)
    end_date = event_date + pd.Timedelta(days=window_days)

    event_df = df[(df["timestamp"] >= start_date) & (df["timestamp"] <= end_date)].copy()
    rolling_corr_event = event_df["BTC_return_daily"].rolling(window=rolling_days).corr(event_df["SP500_return_daily"])

    plt.figure(figsize=(10, 5))
    plt.plot(event_df["timestamp"], rolling_corr_event, marker="o", linestyle="-")
    plt.axhline(0, linestyle="--")
    plt.axvline(event_date, linestyle="--", label="Annonce tarifs Trump")
    plt.xlabel("Date"); plt.ylabel(f"Corrélation glissante {rolling_days} jours")
    plt.title("Corrélation BTC / SP500 autour de l’annonce des tarifs douaniers de Trump")
    plt.legend(); plt.show()
