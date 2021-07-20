import math
import pandas_datareader as dt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

tickers = ['TSLA', 'AAPL', 'FB', 'MSFT', 'GOOGL']
for ticker in tickers:
    data = dt.DataReader(ticker, data_source='yahoo', start='2019-01-01', end='2021-06-18')
    df = pd.DataFrame(data['Close'])
    df["Stock"] = ticker
    df.to_csv('tickers.csv', mode='a')
    newdata = data.filter(['Close'])
    dataset = newdata.values
    data_len = math.ceil(len(dataset) * .75)
    scale = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scale.fit_transform(dataset)
    trained_data = scaled_data[0:data_len, :]
    x_training = []
    y_training = []
    for i in range(60, len(trained_data)):
        x_training.append(trained_data[i - 60:i, 0])
        y_training.append(trained_data[i, 0])
    x_training, y_training = np.array(x_training), np.array(y_training)
    x_training = np.reshape(x_training, (x_training.shape[0], x_training.shape[1], 1))
    my_model = Sequential()
    my_model.add(LSTM(50, return_sequences=True, input_shape=(x_training.shape[1], 1)))
    my_model.add(LSTM(50, return_sequences=False))
    my_model.add(Dense(25))
    my_model.add(Dense(1))
    my_model.compile(optimizer='adam', loss='mean_squared_error')
    my_model.fit(x_training, y_training, batch_size=1, epochs=1)
    test_data = scaled_data[data_len - 60:, :]
    x_test = []
    y_test = dataset[data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i - 60:i, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    predict = my_model.predict(x_test)
    predict = scale.inverse_transform(predict)
    train = data[:data_len]
    current = data[data_len:]
    current['Predictions'] = predict
    ds = pd.DataFrame(current['Predictions'])
    ds["Stock"] = ticker
    ds.to_csv('predictions.csv', mode='a')
