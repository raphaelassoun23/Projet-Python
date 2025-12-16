TICKERS = {
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "SP500": "^GSPC",
    "NASDAQ": "^IXIC",
        # US rates proxies (yields)
    "US10Y": "^TNX",
    "US3M": "^IRX",
    "US30Y": "^TYX",
}

YF_PERIOD = "max"          # identique au notebook
ROLLING_WINDOW_DAYS = 90   # corr glissante principale

EVENT_DATE = "2025-04-05"
EVENT_WINDOW_DAYS = 15
EVENT_ROLLING_DAYS = 10    # notebook: rolling(window=10)
