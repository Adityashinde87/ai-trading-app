from config import ATR_SL_MULTIPLIER, ATR_TARGET_MULTIPLIER, HOLD_CANDLES_15M

def get_trend_1h(df_1h):
    row = df_1h.iloc[-1]

    bullish = (
        row["close"] > row["ema_21"] > row["ema_50"]
        and row["rsi"] > 55
        and row["macd"] > row["macd_signal"]
    )

    bearish = (
        row["close"] < row["ema_21"] < row["ema_50"]
        and row["rsi"] < 45
        and row["macd"] < row["macd_signal"]
    )

    if bullish:
        return "BULLISH"
    if bearish:
        return "BEARISH"
    return "SIDEWAYS"

def get_entry_signal_15m(df_15m, trend_1h):
    row = df_15m.iloc[-1]
    prev = df_15m.iloc[-2]

    bullish_entry = (
        trend_1h == "BULLISH"
        and row["close"] > row["ema_9"] > row["ema_21"]
        and row["rsi"] > 55
        and row["macd"] > row["macd_signal"]
        and prev["close"] <= prev["ema_9"]
    )

    bearish_entry = (
        trend_1h == "BEARISH"
        and row["close"] < row["ema_9"] < row["ema_21"]
        and row["rsi"] < 45
        and row["macd"] < row["macd_signal"]
        and prev["close"] >= prev["ema_9"]
    )

    if bullish_entry:
        return "UP"
    if bearish_entry:
        return "DOWN"
    return "NO TRADE"

def build_trade_plan(df_15m, signal):
    row = df_15m.iloc[-1]
    entry = float(row["close"])
    atr = float(row["atr"]) if row["atr"] == row["atr"] else 20.0

    if signal == "UP":
        stop_loss = round(entry - (atr * ATR_SL_MULTIPLIER), 2)
        target = round(entry + (atr * ATR_TARGET_MULTIPLIER), 2)
        hold_text = f"Hold up to {HOLD_CANDLES_15M} candles on 15m (~1 hour) or till target/SL"
        bias = "Upside breakout probability"
    elif signal == "DOWN":
        stop_loss = round(entry + (atr * ATR_SL_MULTIPLIER), 2)
        target = round(entry - (atr * ATR_TARGET_MULTIPLIER), 2)
        hold_text = f"Hold up to {HOLD_CANDLES_15M} candles on 15m (~1 hour) or till target/SL"
        bias = "Downside breakdown probability"
    else:
        stop_loss = None
        target = None
        hold_text = "Wait for confirmation"
        bias = "No clean entry"

    return {
        "entry": round(entry, 2),
        "stop_loss": stop_loss,
        "target": target,
        "hold_time": hold_text,
        "analysis": bias
    }