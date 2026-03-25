import os

SMARTAPI_API_KEY = os.getenv("SMARTAPI_API_KEY", "RcFPksU9")
SMARTAPI_CLIENT_ID = os.getenv("SMARTAPI_CLIENT_ID", "A775770")
SMARTAPI_PASSWORD = os.getenv("SMARTAPI_PASSWORD", "1171")
SMARTAPI_TOTP_SECRET = os.getenv("SMARTAPI_TOTP_SECRET", "BFAUZ7VATUK5JDABMAJ3FNKB44")

NIFTY_CONFIG = {
    "name": "NIFTY 50",
    "exchange": "NSE",
    "tradingsymbol": "NIFTY",
    "symboltoken": "99926000",
    "analysis_interval": "ONE_HOUR",
    "signal_interval": "FIFTEEN_MINUTE"
}

# Optional ML model paths
MODEL_PATH = "models/nifty_model.pkl"
SCALER_PATH = "models/scaler.pkl"

# Strategy parameters
MIN_CONFIDENCE = 60.0
RISK_REWARD = 2.0
ATR_SL_MULTIPLIER = 1.2
ATR_TARGET_MULTIPLIER = 2.4
HOLD_CANDLES_15M = 4   # around 1 hour