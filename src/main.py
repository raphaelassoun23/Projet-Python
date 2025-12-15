from config import TICKERS, ROLLING_WINDOW_DAYS, EVENT_DATE, EVENT_WINDOW_DAYS, EVENT_ROLLING_DAYS
from fetch import fetch_dataset
from process import build_final_dataset
from visualize import print_correlations, plot_btc_sp500, plot_btc_nasdaq, plot_sp500_nasdaq, plot_event_window

def main() -> None:
    df = fetch_dataset(TICKERS)
    df_final = build_final_dataset(df)

    print_correlations(df_final)
    plot_btc_sp500(df_final, window=ROLLING_WINDOW_DAYS)
    plot_btc_nasdaq(df_final, window=ROLLING_WINDOW_DAYS)
    plot_sp500_nasdaq(df_final, window=ROLLING_WINDOW_DAYS)
    
  
    plot_event_window(df_final, EVENT_DATE, window_days=EVENT_WINDOW_DAYS, rolling_days=EVENT_ROLLING_DAYS)

if __name__ == "__main__":
    main()
