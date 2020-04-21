from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd

class last_five_games(BaseEstimator, TransformerMixin):
    """
    a general class for creating a machine learning step in the machine learning pipeline

    """
    def __init__(self):
        pass
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        df = X.copy()

        home = pd.DataFrame()
        away = pd.DataFrame()

        for team in df['Home'].unique():
            tmp_1 = df.copy()
            tmp_2 = df.copy()
            tmp_1 = tmp_1[['season', 'Wk', 'Home', 'result']]
            tmp_2 = tmp_2[['season', 'Wk', 'Away', 'result']]
            tmp_1 = tmp_1[tmp_1['Home'] == team]
            tmp_2 = tmp_2[tmp_2['Away'] == team]
            columns = ['season', 'Wk', 'team', 'result']
            tmp_1.columns = columns
            tmp_2.columns = columns
            tmp_1['home'] = 1
            tmp_1['last_5_games_home'] = tmp_1['result'].rolling(window=5, min_periods=1).sum()
            tmp_2['home'] = 0
            tmp_2['last_5_games_away'] = tmp_2['result'].rolling(window=5, min_periods=1).sum()
            tmp = tmp_1.append(tmp_2).sort_values(['season', 'Wk'])
            tmp.fillna(method='ffill', inplace=True)
            tmp['last_5_games'] = tmp['result'].rolling(window=5, min_periods=1).sum()
            home = home.append(tmp[tmp['home'] == 1])
            away = away.append(tmp[tmp['home'] == 0])

        home.drop(columns=['season', 'Wk', 'team', 'result', 'home'], inplace=True)
        away.drop(columns=['season', 'Wk', 'team', 'result', 'home'], inplace=True)

        home.columns = ['ht_' + col for col in home.columns]
        away.columns = ['at_' + col for col in away.columns]

        df = df.merge(home, left_index=True, right_index=True).merge(away, left_index=True, right_index=True)

        return df

