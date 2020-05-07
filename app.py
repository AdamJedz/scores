from flask import Flask
import pandas as pd
import os
from datetime import date, datetime

app = Flask(__name__)


@app.route("/")
def home():
    try:
        today = datetime.today()
        min_days = 99
        name = ''
        for file in os.listdir('./predictions'):
            file_date = datetime.strptime(file[-10:-4], '%y%m%d')
            time_delta = (today - file_date).days
            print(time_delta)
            if time_delta < min_days:
                min_days = time_delta
                name = file
        pred = pd.read_csv(f'./predictions/{name}')
        to_print = ''
        for row in pred.iterrows():
            home = row[1]['Home']
            away = row[1]['Away']
            result = row[1]['result']
            if result == 0:
                to_print = to_print + (f'{home} - {away} | Draw<br/>')
            elif result == 1:
                to_print = to_print + (f'{home} - {away} | {home} wins<br/>')
            else:
                to_print = to_print + (f'{home} - {away} | {away} wins<br/>')

        to_print = 'Last predictions: <br/>' + to_print + '<br/><br/>To create newer predictions type "/predict" in the end of web adress.'
        to_print = f'Today is {date.today().strftime("%Y-%m-%d")}.<br/>Last predictions date is 20{name[-10:-8]}-{name[-8:-6]}-{name[-6:-4]}.<nr/><br/>' + to_print
    except:
        to_print = 'No predictions saved!'
    return to_print


@app.route("/predict")
def predict():
    os.system(f'python get_predictions.py 15 19 preds')
    return 'data saved'

@app.route("/preds")
def preds():
    date_1 = datetime.today()
    date_2 = datetime.strptime('200503', '%y%m%d')
    return str((date_1-date_2).days)


if __name__ == "__main__":
    app.run(debug=True)