import os
import pickle
import pandas as pd
from config import MODEL_PATH, SCALER_PATH

class ModelEngine:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_loaded = False
        self._load()

    def _load(self):
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)

            if os.path.exists(SCALER_PATH):
                with open(SCALER_PATH, "rb") as f:
                    self.scaler = pickle.load(f)

            self.model_loaded = True

    def build_feature_row(self, df_15m, df_1h):
        r15 = df_15m.iloc[-1]
        r1h = df_1h.iloc[-1]

        row = pd.DataFrame([{
            "close_15m": r15["close"],
            "rsi_15m": r15["rsi"],
            "ema9_15m": r15["ema_9"],
            "ema21_15m": r15["ema_21"],
            "ema50_15m": r15["ema_50"],
            "macd_15m": r15["macd"],
            "macd_signal_15m": r15["macd_signal"],
            "atr_15m": r15["atr"],
            "return_1_15m": r15["return_1"],
            "return_3_15m": r15["return_3"],
            "volatility_10_15m": r15["volatility_10"],
            "close_1h": r1h["close"],
            "rsi_1h": r1h["rsi"],
            "ema9_1h": r1h["ema_9"],
            "ema21_1h": r1h["ema_21"],
            "ema50_1h": r1h["ema_50"],
            "macd_1h": r1h["macd"],
            "macd_signal_1h": r1h["macd_signal"],
            "atr_1h": r1h["atr"]
        }]).fillna(0)

        return row

    def predict(self, df_15m, df_1h):
        if not self.model_loaded:
            return {
                "ml_signal": "NO TRADE",
                "confidence": 50.0,
                "model_used": False
            }

        X = self.build_feature_row(df_15m, df_1h)

        if self.scaler is not None:
            X_scaled = self.scaler.transform(X)
        else:
            X_scaled = X

        pred = self.model.predict(X_scaled)[0]

        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(X_scaled)[0]
            confidence = float(max(probs) * 100)
        else:
            confidence = 70.0

        signal_map = {
            1: "UP",
            -1: "DOWN",
            0: "NO TRADE"
        }

        return {
            "ml_signal": signal_map.get(pred, "NO TRADE"),
            "confidence": round(confidence, 2),
            "model_used": True
        }

model_engine = ModelEngine()