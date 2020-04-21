from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd

class point_count(BaseEstimator, TransformerMixin):
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
        for year in df['season'].unique():
            for team in df['Home'].unique():
                tmp_1 = df.copy()
                tmp_2 = df.copy()
                tmp_1 = tmp_1[['season', 'Wk', 'Home', 'result']]
                tmp_2 = tmp_2[['season', 'Wk', 'Away', 'result']]
                tmp_1 = tmp_1[(tmp_1['Home'] == team) & (tmp_1['season'] == year)]
                tmp_2 = tmp_2[(tmp_2['Away'] == team) & (tmp_2['season'] == year)]
                tmp_1['points'] = np.where(tmp_1['result'] == 1, 3, np.where(tmp_1['result'] == 0, 1, 0))
                tmp_1['home'] = 1
                tmp_1.rename(columns={'Home': 'team'}, inplace=True)
                tmp_2['points'] = np.where(tmp_2['result'] == 1, 0, np.where(tmp_2['result'] == 0, 1, 3))
                tmp_2['home'] = 0
                tmp_2.rename(columns={'Away': 'team'}, inplace=True)
                tmp = tmp_1.append(tmp_2).sort_values('Wk')
                tmp['points'] = tmp['points'].cumsum()
                home = home.append(tmp[tmp['home'] == 1])
                away = away.append(tmp[tmp['home'] == 0])

        home.rename(columns={'points': 'ht_points'}, inplace=True)
        away.rename(columns={'points': 'at_points'}, inplace=True)

        df = df.merge(home['ht_points'],
                      left_index=True,
                      right_index=True).merge(away['at_points'],
                                              left_index=True,
                                              right_index=True)

        return df

