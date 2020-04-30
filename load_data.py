import argparse
import pandas as pd
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def load_data(year_since, year_to):
    all_seasons = pd.DataFrame()
    for year in range(year_since, year_to + 1):
        if year == 19:
            url = ('https://fbref.com/en/comps/9/schedule/Premier-League-Fixtures')
        else:
            if year == 14:
                marker = 733
            elif year == 15:
                marker = 1467
            elif year == 16:
                marker = 1526
            elif year == 17:
                marker = 1631
            else:
                marker = 1889
            url = 'https://fbref.com/en/comps/9/' + str(marker) + '/schedule/20' + str(year) + '-20' + str(year+1) +'-Premier-League-Fixtures'
        season = pd.read_html(url)[0]

        season['season'] = year

        all_seasons = all_seasons.append(season)

    all_seasons.drop(columns=['Day', 'Date', 'Time', 'xG', 'xG.1', 'Attendance', 'Venue', 'Referee', 'Match Report', 'Notes'], inplace=True)
    newest_week = all_seasons[all_seasons['Score'].isna()]['Wk'].min()
    print(newest_week)
    all_seasons = all_seasons[(~all_seasons['Score'].isna()) | (all_seasons['Wk'] == newest_week)]
    all_seasons.sort_values(['season', 'Wk'], inplace=True)
    all_seasons.reset_index(drop=True, inplace=True)
    return all_seasons

def save_data(data, name):
    data.to_csv('./Data/' + name + '.csv')

if __name__ == '__main__':

    logging.info('Start loading data')
    logging.info('Reading arguments')

    parser = argparse.ArgumentParser(description='Script for downloading game data.')
    parser.add_argument('year_since', type=int)
    parser.add_argument('year_to', type=int)
    parser.add_argument('data_name', type=str)

    args = parser.parse_args()

    year_since, year_to = args.year_since, args.year_to
    name = args.data_name

    logging.info('Loading seasons 20' + str(year_since) + '/20' + str(year_since+1) + ' to 20' + str(year_to) + '/20' + str(year_to+1))
    x = load_data(year_since, year_to)
    logging.info('Data loaded')
    save_data(x, name)
    logging.info('Saved as ' + name + '.csv')