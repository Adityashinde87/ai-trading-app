import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def predict_signal(df):

    # Dummy expansion (real में historical data चाहिए)
    df = pd.concat([df]*20, ignore_index=True)

    # Features
    df["return"] = df["close"].pct_change()
    df["ma_5"] = df["close"].rolling(5).mean()
    df["ma_10"] = df["close"].rolling(10).mean()

    df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)

    df = df.dropna()

    X = df[["close", "return", "ma_5", "ma_10"]]
    y = df["target"]

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    latest = X.tail(1)
    pred = model.predict(latest)

    if pred[0] == 1:
        return "📈 BUY"
    else:
        return "📉 SELL"