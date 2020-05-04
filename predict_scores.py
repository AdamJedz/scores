import argparse
import pandas as pd

from joblib import load
import warnings

from train_model import read_yaml

from datetime import date
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

warnings.filterwarnings('ignore')

def read_data(name):
    path = './data/'
    df = pd.read_csv(path + name + '_processed.csv')
    df = df[df['result'] == 99]
    return df


def transform_data(data, yaml):
    df = data.copy()
    X = df.drop(columns='result')

    pipeline = load(f'./model/{yaml["model_name"]}_transformer.joblib')
    X = pipeline.transform(X)
    return X


def get_predictions(data, yaml):
    model = load(f'./model/{yaml["model_name"]}.joblib')
    y = model.predict(data)
    return y

def save_data(data, y):
    data = data[['season', 'Wk','Home', 'Away']]
    data.reset_index(drop=True, inplace=True)
    data['result'] = y

    today = date.today().strftime('%y%m%d')
    data.to_csv(f'./predictions/preds_{today}.csv')
    return data

if __name__ == '__main__':

    logging.info('Reading arguments')

    parser = argparse.ArgumentParser(description='Script for training score model.')
    parser.add_argument('data_name', type=str)

    args = parser.parse_args()

    name = args.data_name

    logging.info('Reading data')
    x = read_data(name)
    logging.info('Reading YAML file')
    config = read_yaml()
    logging.info('Transforming data')
    X = transform_data(x, config)
    logging.info('Data transformed')
    logging.info('Creating predictions')
    y = get_predictions(X, config)
    logging.info('Saving predictions')
    x = save_data(x, y)
    for row in x.iterrows():
        home = row[1]['Home']
        away = row[1]['Away']
        result = row[1]['result']
        if result == 0:
            print(f'{home} - {away} | Draw')
        elif result == 1:
            print(f'{home} - {away} | {home} wins')
        else:
            print(f'{home} - {away} | {away} wins')



