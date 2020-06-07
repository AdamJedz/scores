# Premier League Scores prediction  
  
  
Based on data from https://fbref.com I created model that predicts outcome of football game. Model is built on logistic regression with tuned hyperparameters.  
  

## Structure  
  
* load_data.py - script to load data from website with scores. Takes 3 inputs (year_since (int), year_to (int), name(str) e.g. 15 19 test). Saves data in *data* folder,  
* preprocess_data.py - script to create multiple features from data (e.g. # of home wins, # of home goals etc. All features are in model/model.yaml). Takes string as an input. Saves data in *data* folder,
* train_model.py - script to create and save model based on preprocessed data. Model parameteres are in model/model.yaml file. Takes string as an input. Saves model and transformer as joblib files in *model* folder,
* predict_scores.py - creates prediction based on preprocess data and created model. Takes string as an input. Saves predictions in *predictions* folder,


## Usage  

1. Load data ('python3 load_data.py 15 19 test'),  
2. Preprocess data ('python3 preprocess_data.py test'),  
3. Train model ('python3 train_model.py test'),  
4. Predict scores ('python3 predict_scores.py test').  

If model is trained you can load and preprocess data using get_predictions.py script ('python3 get_predictions.py 15 19 test').  

For every game there are 3 possible outcomes:  
* 1 - home team wins,  
* -1 - away team wins,  
* 0 - draw.  

Predictions are made for soonest game week (or if week is in progress predictions ae only for games that are left in current game week). 

# Web app
Application is avalaible on https://adamiecscores.azurewebsites.net/
