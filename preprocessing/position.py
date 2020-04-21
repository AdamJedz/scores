from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd

class positioner(BaseEstimator, TransformerMixin):
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
            for week in df['Wk'].unique():
                tmp_1 = df[(df['Wk'] == week) & (df['season'] == year)].copy()
                tmp_2 = df[(df['Wk'] == week) & (df['season'] == year)].copy()

                tmp_1 = tmp_1[['Home', 'ht_points',
                               'goals_for_home', 'goals_against_home']]
                tmp_1.rename(columns={'Home': 'team', 'ht_points': 'points',
                                      'goals_for_home': 'goals_for', 'goals_against_home': 'goals_against'},
                             inplace=True)
                tmp_1['home'] = 1

                tmp_2 = tmp_2[['Away', 'at_points',
                               'goals_for_away', 'goals_against_away']]
                tmp_2.rename(columns={'Away': 'team', 'at_points': 'points',
                                      'goals_for_away': 'goals_for', 'goals_against_away': 'goals_against'},
                             inplace=True)
                tmp_2['home'] = 0

                tmp = tmp_1.append(tmp_2)
                tmp['goal_diff'] = tmp['goals_for'] - tmp['goals_against']
                tmp.sort_values(['points', 'goals_for', 'goal_diff'], ascending=False, inplace=True)
                tmp['position'] = range(1, len(tmp) + 1)
                home = home.append(tmp[tmp['home'] == 1])
                away = away.append(tmp[tmp['home'] == 0])

        home.rename(columns={'position': 'ht_position', 'goal_diff': 'ht_goal_diff'}, inplace=True)
        away.rename(columns={'position': 'at_position', 'goal_diff': 'at_goal_diff'}, inplace=True)

        df = df.merge(home[['ht_position', 'ht_goal_diff']],
                      left_index=True,
                      right_index=True).merge(away[['at_position', 'at_goal_diff']],
                                              left_index=True,
                                              right_index=True)

        return df

