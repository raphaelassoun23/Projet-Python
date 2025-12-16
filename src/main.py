from config import TICKERS, ROLLING_WINDOW_DAYS, EVENT_DATE, EVENT_WINDOW_DAYS, EVENT_ROLLING_DAYS
from fetch import fetch_dataset
from process import build_final_dataset
from visualize import print_correlations, plot_btc_sp500, plot_btc_nasdaq, plot_sp500_nasdaq, plot_event_window, plot_btc_and_us10y, plot_rolling_corr, plot_scatter_returns, plot_event_study_rate_shocks, plot_btc_vs_slope

def main() -> None:
    df = fetch_dataset(TICKERS)
    df_final = build_final_dataset(df)

    print_correlations(df_final)
    plot_btc_sp500(df_final, window=ROLLING_WINDOW_DAYS)
    plot_btc_nasdaq(df_final, window=ROLLING_WINDOW_DAYS)
    plot_sp500_nasdaq(df_final, window=ROLLING_WINDOW_DAYS)
    
  
    plot_event_window(df_final, EVENT_DATE, window_days=EVENT_WINDOW_DAYS, rolling_days=EVENT_ROLLING_DAYS)
    plot_btc_and_us10y(df_final)
    plot_rolling_corr(df_final, window=60)
    plot_scatter_returns(df_final)
    plot_event_study_rate_shocks(df_final, shock_quantile=0.99, pre=5, post=10)

if __name__ == "__main__":
    main()
