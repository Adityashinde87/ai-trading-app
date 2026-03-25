import pandas as pd
import numpy as np

def add_rsi(df, period=14):
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["rsi"] = 100 - (100 / (1 + rs))
    return df

def add_ema(df, span):
    df[f"ema_{span}"] = df["close"].ewm(span=span, adjust=False).mean()
    return df

def add_macd(df):
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]
    return df

def add_atr(df, period=14):
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["atr"] = tr.rolling(period).mean()
    return df

def add_features(df):
    df = df.copy()
    df = add_ema(df, 9)
    df = add_ema(df, 21)
    df = add_ema(df, 50)
    df = add_rsi(df, 14)
    df = add_macd(df)
    df = add_atr(df, 14)

    df["return_1"] = df["close"].pct_change()
    df["return_3"] = df["close"].pct_change(3)
    df["volatility_10"] = df["return_1"].rolling(10).std()

    return df

def enrich_all(df_15m, df_1h):
    return add_features(df_15m), add_features(df_1h)