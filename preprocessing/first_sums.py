from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd

class first_sums(BaseEstimator, TransformerMixin):
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
                tmp_1 = tmp_1[(tmp_1['Home'] == team) & (tmp_1['season'] == year)]
                tmp_1 = tmp_1[['season', 'Wk', 'Home', 'home_win',
                               'home_draw', 'home_lose', 'goals_home', 'goals_away']]
                tmp_1.rename(columns={'Home': 'team', 'home_win': 'win', 'home_draw': 'draw',
                                      'home_lose': 'lose', 'goals_home': 'goals_for', 'goals_away': 'goals_against'},
                             inplace=True)
                tmp_1['home'] = 1

                tmp_2 = tmp_2[(tmp_2['Away'] == team) & (tmp_2['season'] == year)]
                tmp_2 = tmp_2[['season', 'Wk', 'Away', 'away_win',
                               'away_draw', 'away_lose', 'goals_away', 'goals_home']]
                tmp_2.rename(columns={'Away': 'team', 'away_win': 'win', 'away_draw': 'draw',
                                      'away_lose': 'lose', 'goals_away': 'goals_for', 'goals_home': 'goals_against'},
                             inplace=True)
                tmp_2['home'] = 0

                tmp = tmp_1.append(tmp_2)
                tmp.sort_values(['season', 'Wk'], inplace=True)
                tmp[['win', 'draw', 'lose', 'goals_for', 'goals_against']] = tmp[[
                    'win', 'draw', 'lose', 'goals_for', 'goals_against']].transform('cumsum')
                home = home.append(tmp[tmp['home'] == 1].drop(columns='home'))
                away = away.append(tmp[tmp['home'] == 0].drop(columns='home'))

        home.columns = [col + '_home' for col in home.columns]
        df = df.merge(home.drop(columns=['season_home', 'Wk_home', 'team_home']),
                      left_index=True,
                      right_index=True)

        away.columns = [col + '_away' for col in away.columns]
        df = df.merge(away.drop(columns=['season_away', 'Wk_away', 'team_away']),
                      left_index=True,
                      right_index=True)

        df[['ht_home_win', 'ht_home_draw', 'ht_home_lose', 'ht_home_goals_for', 'ht_home_goals_against']] = \
        df.groupby(['season', 'Home'])[['home_win', 'home_draw', 'home_lose', 'goals_home', 'goals_away']].transform(
            'cumsum')
        df[['at_home_win', 'at_home_draw', 'at_home_lose', 'at_home_goals_for', 'at_home_goals_against']] = \
        df.groupby(['season', 'Away'])[['away_win', 'away_draw', 'away_lose', 'goals_home', 'goals_away']].transform(
            'cumsum')

        df.drop(columns=['home_win', 'home_draw', 'home_lose', 'goals_home', 'goals_away', 'away_win', 'away_draw',
                         'away_lose'], inplace=True)

        return df

