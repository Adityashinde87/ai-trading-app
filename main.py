from data_fetch import get_data
from model import predict_signal

data = get_data()

if data is not None:
    result = predict_signal(data)
    print("Signal:", result)
else:
    print("No data received")