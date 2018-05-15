import sys
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor


def get_data(playerID):
    df = pd.read_csv('src/data/condensed.csv').set_index('playerID')
    X_rest = df[df.index != playerID]
    y_rest = X_rest.pop('year7_avg')
    X1 = df[df.index == playerID]
    y1 = X1.pop('year7_avg')

    return df, df.pop('year7_avg'), X_rest, y_rest, X1, y1

def get_import_feats(X, y):
    tree = fit_forest(X, y)
    feat_imports = tree.feature_importances_
    return np.where(feat_imports > 0)[0]

def fit_forest(X, y):
    return RandomForestRegressor(max_depth=4).fit(X, y)

def display_results(model, X, y):
    results = pd.DataFrame(y)
    results.columns = ['actual']
    results['predicted'] = model.predict(X)
    results = results.round(3)
    results['difference'] = (results['actual'] - results['predicted']).abs()
    print(results.round(3))


if __name__ == '__main__':
    playerID = sys.argv[1]
    X_all, y_all, X_rest, y_rest, X1, y1 = get_data(playerID)
    important_feats = get_import_feats(X_all, y_all)
    X_rest = X_rest.iloc[:, important_feats]
    X1 = X1.iloc[:, important_feats]
    forest = fit_forest(X_rest, y_rest)
    display_results(forest, X1, y1)
