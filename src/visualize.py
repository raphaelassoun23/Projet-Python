import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

def _ensure_datetime(df: pd.DataFrame) -> pd.DataFrame:
    if "timestamp" not in df.columns:
        raise KeyError("Colonne 'timestamp' manquante.")
    out = df.copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"])
    return out.sort_values("timestamp")

def _col(df: pd.DataFrame, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    raise ValueError(f"Aucune colonne trouvée parmi: {candidates}")

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

    # -----------------------------
# 1) Prix BTC + taux (US10Y) sur 2 axes
# -----------------------------
def plot_btc_and_us10y(df: pd.DataFrame, btc_price_col="BTC_price", us10y_col="US10Y_price", log_btc=True):
    df = _ensure_datetime(df)
    if btc_price_col not in df.columns or us10y_col not in df.columns:
        raise ValueError(f"Colonnes manquantes: {btc_price_col} et/ou {us10y_col}")

    fig, ax1 = plt.subplots(figsize=(12, 4))
    ax1.plot(df["timestamp"], df[btc_price_col], label=btc_price_col)
    ax1.set_ylabel("BTC price")
    if log_btc:
        ax1.set_yscale("log")
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(df["timestamp"], df[us10y_col], label=us10y_col)
    ax2.set_ylabel("US10Y (proxy yield)")

    plt.title("BTC vs US10Y (prix / yield proxy)")
    fig.tight_layout()
    plt.show()

# -----------------------------
# 2) Corrélation glissante BTC returns vs ΔUS10Y
# -----------------------------
def plot_rolling_corr(df: pd.DataFrame, window=60,
                      btc_ret_col="BTC_return_daily", us10y_ret_col="US10Y_return_daily"):
    df = _ensure_datetime(df)
    for c in [btc_ret_col, us10y_ret_col]:
        if c not in df.columns:
            raise ValueError(f"Colonne manquante: {c}")

    d = df[["timestamp", btc_ret_col, us10y_ret_col]].dropna()
    corr = d[btc_ret_col].rolling(window).corr(d[us10y_ret_col])

    plt.figure(figsize=(12, 4))
    plt.plot(d["timestamp"], corr)
    plt.axhline(0, linewidth=1)
    plt.title(f"Corrélation glissante ({window}j) : BTC returns vs ΔUS10Y")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# -----------------------------
# 3) Scatter BTC returns vs ΔUS10Y (avec binnings de volatilité BTC)
# -----------------------------
def plot_scatter_returns(df: pd.DataFrame,
                         btc_ret_col="BTC_return_daily",
                         us10y_ret_col="US10Y_return_daily",
                         btc_vol_col=None,
                         vol_window=30):
    df = _ensure_datetime(df)
    for c in [btc_ret_col, us10y_ret_col]:
        if c not in df.columns:
            raise ValueError(f"Colonne manquante: {c}")

    d = df[[btc_ret_col, us10y_ret_col]].dropna().copy()

    # si pas de vol fournie, on la construit via rolling std
    if btc_vol_col is None:
        d["btc_vol"] = d[btc_ret_col].rolling(vol_window).std()
        btc_vol_col = "btc_vol"
    else:
        if btc_vol_col not in df.columns:
            raise ValueError(f"Colonne vol manquante: {btc_vol_col}")
        d[btc_vol_col] = df.loc[d.index, btc_vol_col]

    d = d.dropna(subset=[btc_vol_col])

    # binning en terciles de vol (low/med/high)
    q1, q2 = d[btc_vol_col].quantile([1/3, 2/3])
    d["vol_regime"] = np.where(d[btc_vol_col] <= q1, "low",
                       np.where(d[btc_vol_col] <= q2, "mid", "high"))

    plt.figure(figsize=(7, 6))
    for regime in ["low", "mid", "high"]:
        m = d["vol_regime"] == regime
        plt.scatter(d.loc[m, us10y_ret_col], d.loc[m, btc_ret_col], s=10, label=regime)

    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)
    plt.title("Scatter : BTC returns vs ΔUS10Y (coloré par régime de vol BTC)")
    plt.xlabel("ΔUS10Y (daily)")
    plt.ylabel("BTC log-return (daily)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

# -----------------------------
# 4) “Event study” : BTC autour des jours de gros mouvements de taux
# -----------------------------
def plot_event_study_rate_shocks(df: pd.DataFrame,
                                 us10y_ret_col="US10Y_return_daily",
                                 btc_ret_col="BTC_return_daily",
                                 shock_quantile=0.99,
                                 pre=5, post=10):
    """
    Sélectionne les jours où |ΔUS10Y| est très grand (quantile),
    puis trace le retour moyen cumulé de BTC autour de l'événement.
    """
    df = _ensure_datetime(df)
    for c in [us10y_ret_col, btc_ret_col]:
        if c not in df.columns:
            raise ValueError(f"Colonne manquante: {c}")

    d = df[["timestamp", us10y_ret_col, btc_ret_col]].dropna().reset_index(drop=True)
    thr = d[us10y_ret_col].abs().quantile(shock_quantile)

    event_idx = d.index[d[us10y_ret_col].abs() >= thr].to_list()
    if len(event_idx) == 0:
        raise ValueError("Aucun événement détecté (seuil trop élevé ou données insuffisantes).")

    # construire matrice des fenêtres autour d'événements
    window = np.arange(-pre, post + 1)
    paths = []
    for i in event_idx:
        if i - pre < 0 or i + post >= len(d):
            continue
        r = d.loc[i - pre:i + post, btc_ret_col].to_numpy()
        cum = np.cumsum(r)  # cum log-returns
        paths.append(cum)

    if len(paths) == 0:
        raise ValueError("Événements détectés mais aucun n'a une fenêtre complète (pré/post).")

    avg = np.mean(np.vstack(paths), axis=0)

    plt.figure(figsize=(10, 4))
    plt.plot(window, avg)
    plt.axvline(0, linewidth=1)
    plt.title(f"Event study : BTC autour des chocs de taux (|ΔUS10Y| >= q{shock_quantile})")
    plt.xlabel("Jours relatifs à l'événement")
    plt.ylabel("Cumul log-returns BTC (moyenne)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# -----------------------------
# 5) Si vous avez la pente (10Y-3M) : BTC vs slope
# -----------------------------
def plot_btc_vs_slope(df: pd.DataFrame, slope_col="US_slope_10Y_3M", btc_ret_col="BTC_return_daily"):
    df = _ensure_datetime(df)
    for c in [slope_col, btc_ret_col]:
        if c not in df.columns:
            raise ValueError(f"Colonne manquante: {c}")

    d = df[[slope_col, btc_ret_col]].dropna()
    plt.figure(figsize=(7, 6))
    plt.scatter(d[slope_col], d[btc_ret_col], s=10)
    plt.axhline(0, linewidth=1)
    plt.title("BTC returns vs pente de courbe (10Y-3M)")
    plt.xlabel(slope_col)
    plt.ylabel(btc_ret_col)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
