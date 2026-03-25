from flask import Flask, render_template, jsonify
from data_fetch import get_ltp, get_15m_data, get_1h_data
from indicators import enrich_all
from signal_engine import combine_signals
from utils import now_text, safe_round
import time

app = Flask(__name__)

CACHE = {
    "data": None,
    "time": 0
}

CACHE_SECONDS = 60

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/signal")
def api_signal():
    try:
        now = time.time()

        if CACHE["data"] is not None and (now - CACHE["time"] < CACHE_SECONDS):
            return jsonify(CACHE["data"])

        ltp = get_ltp()
        df_15m = get_15m_data()
        df_1h = get_1h_data()

        df_15m, df_1h = enrich_all(df_15m, df_1h)
        result = combine_signals(df_15m, df_1h)

        last15 = df_15m.iloc[-1]
        last1h = df_1h.iloc[-1]

        response = {
            "status": "success",
            "symbol": "NIFTY 50",
            "live_price": safe_round(ltp),
            "final_signal": result.get("final_signal", "NO TRADE"),
            "trend_1h": result.get("trend_1h", "SIDEWAYS"),
            "rule_signal": result.get("rule_signal", "NO TRADE"),
            "ml_signal": result.get("ml_signal", "NO TRADE"),
            "confidence": safe_round(result.get("confidence", 50)),
            "entry": result.get("entry"),
            "stop_loss": result.get("stop_loss"),
            "target": result.get("target"),
            "hold_time": result.get("hold_time", "Wait for confirmation"),
            "analysis": result.get("analysis", "No clean entry"),
            "rsi_15m": safe_round(last15.get("rsi")),
            "ema9_15m": safe_round(last15.get("ema_9")),
            "ema21_15m": safe_round(last15.get("ema_21")),
            "rsi_1h": safe_round(last1h.get("rsi")),
            "ema21_1h": safe_round(last1h.get("ema_21")),
            "ema50_1h": safe_round(last1h.get("ema_50")),
            "updated_at": now_text(),
            "price_series": [safe_round(x) for x in df_15m["close"].tail(20).tolist()]
        }

        CACHE["data"] = response
        CACHE["time"] = now

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "symbol": "NIFTY 50",
            "live_price": "--",
            "final_signal": "NO TRADE",
            "trend_1h": "SIDEWAYS",
            "rule_signal": "NO TRADE",
            "ml_signal": "NO TRADE",
            "confidence": 50,
            "entry": "--",
            "stop_loss": "--",
            "target": "--",
            "hold_time": "Wait for confirmation",
            "analysis": "Live data fetch failed",
            "rsi_15m": "--",
            "ema9_15m": "--",
            "ema21_15m": "--",
            "rsi_1h": "--",
            "ema21_1h": "--",
            "ema50_1h": "--",
            "updated_at": now_text(),
            "price_series": []
        }), 200

if __name__ == "__main__":
    app.run(debug=True)