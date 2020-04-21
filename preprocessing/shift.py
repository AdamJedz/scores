from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd

class shifter(BaseEstimator, TransformerMixin):
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
                tmp_1 = tmp_1[['season', 'Wk', 'Home', 'win_home', 'draw_home', 'lose_home', 'goals_for_home',
                               'goals_against_home', 'ht_home_win', 'ht_home_draw', 'ht_home_lose', 'ht_home_goals_for',
                               'ht_home_goals_against', 'ht_points', 'ht_position', 'ht_goal_diff']]
                tmp_2 = tmp_2[['season', 'Wk', 'Away', 'win_away', 'draw_away', 'lose_away', 'goals_for_away',
                               'goals_against_away', 'at_home_win', 'at_home_draw', 'at_home_lose',
                               'at_home_goals_for', 'at_home_goals_against', 'at_points', 'at_position',
                               'at_goal_diff']]
                tmp_1 = tmp_1[(tmp_1['Home'] == team) & (tmp_1['season'] == year)]
                tmp_2 = tmp_2[(tmp_2['Away'] == team) & (tmp_2['season'] == year)]
                columns = ['season', 'Wk', 'team', 'win', 'draw', 'lose', 'goals_for', 'goals_against',
                           'home_win', 'home_draw', 'home_lose', 'home_goals_for', 'home_goals_against', 'points',
                           'position', 'goal_diff']
                tmp_1.columns = columns
                tmp_2.columns = columns
                tmp_1['home'] = 1
                tmp_2['home'] = 0

                tmp = tmp_1.append(tmp_2).sort_values('Wk')

                tmp[tmp.columns[3:-1]] = tmp[tmp.columns[3:-1]].shift(1)
                tmp.fillna(0, inplace=True)
                home = home.append(tmp[tmp['home'] == 1])
                away = away.append(tmp[tmp['home'] == 0])

        home.drop(columns=['season', 'Wk', 'team', 'home'], inplace=True)
        away.drop(columns=['season', 'Wk', 'team', 'home'], inplace=True)

        home.columns = ['ht_' + col for col in home.columns]
        away.columns = ['at_' + col for col in away.columns]

        df = df[['season', 'Wk', 'Home', 'Away', 'result']].merge(home,
                                                                  left_index=True,
                                                                  right_index=True).merge(away,
                                                                                          left_index=True,
                                                                                          right_index=True)

        return df

