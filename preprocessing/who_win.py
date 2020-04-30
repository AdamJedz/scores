from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd

class create_winner(BaseEstimator, TransformerMixin):
    """
    a general class for creating a machine learning step in the machine learning pipeline

    """
    def __init__(self):
        pass
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):

        df = X.copy()
        def who_win(score):

            try:
                score = score.split('–')
                goals_home = score[0]
                goals_away = score[1]

                if goals_home > goals_away:
                    result = 1

                    home_win = 1
                    home_draw = 0
                    home_lose = 0

                    away_win = 0
                    away_draw = 0
                    away_lose = 1

                elif goals_home < goals_away:
                    result = -1

                    home_win = 0
                    home_draw = 0
                    home_lose = 1

                    away_win = 1
                    away_draw = 0
                    away_lose = 0

                else:
                    result = 0

                    home_win = 0
                    home_draw = 1
                    home_lose = 0

                    away_win = 0
                    away_draw = 1
                    away_lose = 0



            except:
                result = 99

                home_win = 99
                home_draw = 99
                home_lose = 99

                away_win = 99
                away_draw = 99
                away_lose = 99

                goals_away = 99
                goals_home = 99

            return home_win, home_draw, home_lose, goals_home, away_win, away_draw, away_lose, goals_away, result

        tmp = df.apply(lambda x: who_win(x['Score']), 1)
        home_win = []
        home_draw = []
        home_lose = []
        goals_home = []
        away_win = []
        away_draw = []
        away_lose = []
        goals_away = []
        result = []
        for i in tmp:
            home_win.append(i[0])
            home_draw.append(i[1])
            home_lose.append(i[2])
            goals_home.append(i[3])
            away_win.append(i[4])
            away_draw.append(i[5])
            away_lose.append(i[6])
            goals_away.append(i[7])
            result.append(i[8])

        df['home_win'] = home_win
        df['home_draw'] = home_draw
        df['home_lose'] = home_lose
        df['goals_home'] = goals_home
        df['away_win'] = away_win
        df['away_draw'] = away_draw
        df['away_lose'] = away_lose
        df['goals_away'] = goals_away
        df['result'] = result
        df['goals_home'] = df['goals_home'].astype(int)
        df['goals_away'] = df['goals_away'].astype(int)
        return df

