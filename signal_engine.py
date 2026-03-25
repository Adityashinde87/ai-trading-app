from config import MIN_CONFIDENCE
from strategy import get_trend_1h, get_entry_signal_15m, build_trade_plan
from model import model_engine

def combine_signals(df_15m, df_1h):
    trend_1h = get_trend_1h(df_1h)
    rule_signal = get_entry_signal_15m(df_15m, trend_1h)

    ml_result = model_engine.predict(df_15m, df_1h)
    ml_signal = ml_result["ml_signal"]
    confidence = ml_result["confidence"]

    # final logic
    if not ml_result["model_used"]:
        final_signal = rule_signal
    else:
        if confidence < MIN_CONFIDENCE:
            final_signal = "NO TRADE"
        elif rule_signal == ml_signal and rule_signal != "NO TRADE":
            final_signal = rule_signal
        else:
            final_signal = "NO TRADE"

    trade_plan = build_trade_plan(df_15m, final_signal)

    return {
        "trend_1h": trend_1h,
        "rule_signal": rule_signal,
        "ml_signal": ml_signal,
        "confidence": confidence,
        "final_signal": final_signal,
        **trade_plan
    }