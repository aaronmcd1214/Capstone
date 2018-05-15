import sys
import pandas as pd
import numpy as np

from collections import defaultdict

from keras.models import Sequential
from keras.layers import Dense, BatchNormalization, LSTM, Dropout

from sklearn.preprocessing import normalize


def get_data(playerID):
    print('Getting data...')
    df = pd.read_csv('src/data/uncondensed.csv')
    df.drop(['Unnamed: 0', 'yearID'], axis=1, inplace=True)
    df = pd.get_dummies(df, columns=['pos'])
    df.set_index('playerID', inplace=True, drop=True)

    X = df.groupby('playerID').head(6)
    y = pd.DataFrame(df['avg'].groupby('playerID').tail(6))

    playerID = check_player(X, playerID) # checks if playerID is in dataset
    # separate interested player from group
    X1 = X[X.index == playerID]
    y1 = y[y.index == playerID]

    X_all = X[X.index != playerID]
    y_all = y[y.index != playerID]

    return X_all, y_all, X1, y1

def check_player(df, playerID):
    exists = False
    while exists == False:
        if playerID == 'q':
            sys.exit()
        elif playerID in df.index:
            return playerID
        else:
            playerID = input("Please try another playerID or enter 'q' to quit: ")

def dict_convert(df):
    length = pd.value_counts(df.index)[0]
    def_dict = defaultdict(dict)
    if length == 1:
        return df.T.to_dict()
    for i in range(length):
        year = 'year' + str(i + 1)
        def_dict[year] = df.groupby('playerID').nth(i).T.to_dict('index')
    return def_dict

def format_data(X_df, y_df):
    # convert to dicts
    X_dict = dict_convert(X_df)
    y_dict = dict_convert(y_df)
    # convert to panels
    X_panel = pd.Panel(X_dict)
    y_panel = pd.Panel(y_dict)
    # convert to matrices
    X_mat = X_panel.as_matrix().astype('float32')
    y_mat = y_panel.as_matrix().astype('float32')
    # reorganize axis
    X_mat = np.moveaxis(X_mat, 0, 1)
    y_mat = np.moveaxis(y_mat, 0, 1)

    y_mat = y_mat[:,-1,:]

    return X_mat, y_mat

def fit_lstm(X_train, y_train):
    print('Training LSTM Model...')
    lstm_model = Sequential()
    lstm_model.add(LSTM(28, input_shape=(6, 22), return_sequences=True))
    lstm_model.add(BatchNormalization())
    lstm_model.add(Dropout(.3))
    lstm_model.add(LSTM(28))
    lstm_model.add(BatchNormalization())
    lstm_model.add(Dense(64))
    lstm_model.add(Dense(1))
    lstm_model.compile(loss='mean_squared_error', optimizer='adam')
    lstm_model.fit(X_train, y_train, verbose=0, epochs=100, batch_size=10)

    return lstm_model

def display_results(model, X_test, y_test):
    y_pred = model.predict(X_test)
    df = pd.DataFrame(y_test)
    df.columns = ['actual']
    df['predicted'] = y_pred
    df = df.round(3)
    df['difference'] = (df['actual'] - df['predicted']).abs()
    print(df)

if __name__ == '__main__':
    playerID = sys.argv[1]
    X_df_all, y_df_all, X_df_1, y_df_1 = get_data(playerID) # get initial dataset and format
    print('Formatting data...')
    X1_format, y1_format = format_data(X_df_1, y_df_1) # format dataset
    X_all_format, y_all_format = format_data(X_df_all, y_df_all)
    lstm_model = fit_lstm(X_all_format, y_all_format)
    display_results(lstm_model, X1_format, y1_format)
