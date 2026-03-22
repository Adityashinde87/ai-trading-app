from flask import Flask, render_template, request
from data_fetch import get_data
from model import predict_signal

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = get_data()

    if data is not None:
        signal = predict_signal(data)
        price = data["close"].iloc[-1]
        return render_template("index.html", signal=signal, price=price)
    else:
        return render_template("index.html", signal="No data received", price=None)

if __name__ == "__main__":
    app.run(debug=True)