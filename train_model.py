import argparse
import pandas as pd

from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression

from joblib import dump
import yaml

import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def read_data(name):
    path = './data/'
    df = pd.read_csv(path + name + '_processed.csv')
    df = df[df['result'] != 99]
    return df


def read_yaml():
    with open('./model/model.yaml') as y:
        desc = yaml.load(y, Loader=yaml.FullLoader)
    return desc


def transform_data(data, yaml):
    df = data.copy()
    X = df.drop(columns='result')
    y = df['result']

    pipeline = ColumnTransformer([
        ('numerical_transformations', StandardScaler(), yaml['numerical_features']),
        ('categorical_transformations', OrdinalEncoder(), yaml['categorical_features'])
    ])

    pipeline.fit(X)
    X = pipeline.transform(X)

    dump(pipeline, f'./model/{yaml["model_name"]}_transformer.joblib')
    yaml['transformer'] = f'{yaml["model_name"]}_transformer.joblib'
    return X, y


def train_model(X, y, yaml):
    model = LogisticRegression(random_state=0, **yaml['hiperparameters'])
    model.fit(X,y)

    dump(model, f'./model/{yaml["model_name"]}.joblib')

    return model.score(X,y)

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
    X, y = transform_data(x, config)
    logging.info('Data transformed')
    logging.info(f'Transformed saved as {config["model_name"]}_transformer.joblib')
    logging.info('Model training')
    score = train_model(X, y, config)
    logging.info(f'Model accuracy: {score*100:.2f}%')
    logging.info(f'Model saved as {config["model_name"]}.joblib')



