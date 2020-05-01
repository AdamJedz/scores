import os
import argparse

def run_everything(name, year_since, year_to):
    os.system(f'python load_data.py {year_since} {year_to} {name}')
    os.system(f'python preprocess_data.py {name}')
    os.system(f'python predict_scores.py {name}')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Script for downloading game data.')
    parser.add_argument('year_since', type=int)
    parser.add_argument('year_to', type=int)
    parser.add_argument('data_name', type=str)

    args = parser.parse_args()

    year_since, year_to = args.year_since, args.year_to
    name = args.data_name

    run_everything(name, year_since, year_to)
