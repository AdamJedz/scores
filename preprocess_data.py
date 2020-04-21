import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from preprocessing.who_win import create_winner
from preprocessing.first_sums import first_sums
from preprocessing.points import point_count
from preprocessing.position import positioner
from preprocessing.shift import shifter
from preprocessing.five_games import last_five_games

import warnings
import logging
import argparse

warnings.filterwarnings('ignore')


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def read_data(name):
    path = './data/'
    df = pd.read_csv(path + name + '.csv')
    return df

def feature_add_pipeline():
    return Pipeline([
        ('create_winner', create_winner()),
        ('win/lose/draw sums', first_sums()),
        ('count_points', point_count()),
        ('positions', positioner()),
        ('shift_by_one', shifter()),
        ('analyze_last_5_games', last_five_games())
    ])

def save_data(data, name):
    data.to_csv('./data/' + name + '_processed.csv')

if __name__ == '__main__':

    logging.info('Start preprocessing data')
    logging.info('Reading arguments')

    parser = argparse.ArgumentParser(description='Script for add features to game data.')
    parser.add_argument('data_name', type=str)
    args = parser.parse_args()
    name = args.data_name

    x = read_data(name)
    logging.info('Data loaded')

    pipe = feature_add_pipeline()
    x = pipe.fit_transform(x)
    logging.info('Features added')

    save_data(x, name)

    logging.info('Saved as ' + name + '_processed.csv')
