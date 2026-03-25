from SmartApi import SmartConnect
import pyotp
import pandas as pd
from datetime import datetime, timedelta
import time

from config import (
    SMARTAPI_API_KEY,
    SMARTAPI_CLIENT_ID,
    SMARTAPI_PASSWORD,
    SMARTAPI_TOTP_SECRET,
    NIFTY_CONFIG
)

def get_smartapi_client():
    obj = SmartConnect(api_key=SMARTAPI_API_KEY)
    totp = pyotp.TOTP(SMARTAPI_TOTP_SECRET).now()
    session = obj.generateSession(SMARTAPI_CLIENT_ID, SMARTAPI_PASSWORD, totp)

    if not session.get("status"):
        raise Exception(f"SmartAPI login failed: {session}")

    return obj

def get_ltp():
    client = get_smartapi_client()
    resp = client.ltpData(
        exchange=NIFTY_CONFIG["exchange"],
        tradingsymbol=NIFTY_CONFIG["tradingsymbol"],
        symboltoken=NIFTY_CONFIG["symboltoken"]
    )

    if not resp.get("status"):
        raise Exception(f"LTP fetch failed: {resp}")

    return float(resp["data"]["ltp"])

def _fetch_candles(interval, days_back=20, retries=3, delay=2):
    client = get_smartapi_client()

    to_date = datetime.now()
    from_date = to_date - timedelta(days=days_back)

    params = {
        "exchange": NIFTY_CONFIG["exchange"],
        "symboltoken": NIFTY_CONFIG["symboltoken"],
        "interval": interval,
        "fromdate": from_date.strftime("%Y-%m-%d %H:%M"),
        "todate": to_date.strftime("%Y-%m-%d %H:%M")
    }

    last_error = None

    for attempt in range(retries):
        resp = client.getCandleData(params)

        if resp.get("status") and resp.get("data"):
            df = pd.DataFrame(
                resp["data"],
                columns=["datetime", "open", "high", "low", "close", "volume"]
            )
            df["datetime"] = pd.to_datetime(df["datetime"])
            num_cols = ["open", "high", "low", "close", "volume"]
            df[num_cols] = df[num_cols].astype(float)
            df = df.sort_values("datetime").reset_index(drop=True)
            return df

        last_error = resp
        time.sleep(delay)

    raise Exception(f"Candle fetch failed for {interval}: {last_error}")

def get_15m_data():
    return _fetch_candles(NIFTY_CONFIG["signal_interval"], days_back=20)

def get_1h_data():
    return _fetch_candles(NIFTY_CONFIG["analysis_interval"], days_back=60)