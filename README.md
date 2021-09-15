# Tennis Match Predictor
A library of ML functions for predicting the winners of tennis matches

Data is sourced via [JeffSackmann](https://github.com/JeffSackmann), and his accompanying website [www.tennisabstract.com](http://www.tennisabstract.com/)

## What each script does
### `compile_data.py`
* Iterates over a supplied CSV file of matches (like those found in the `data` directory), parsing the names of the participants and the outcome.
* Scrapes the statistics of the participants of the supplied matches, building a pandas dataframe.  Admittedly, it isn't very good at this, due to slight variations in player names.  Any match that the scraper can't get good statistics for one of the participants is scrapped.
* Builds a dataframe of the matches, the statistics of the participants, and the outcome.
* Parameters:
  1. input .csv file path
  2. output .csv file path
* Example:
```
python3 compile_data.py data/last_5.csv compiled_statistics.csv
```

### train_model.py
* Using the output from the previous script, cleans the data, then trains a model based on it.  The library being used is an sklearn classifier.
* The trained model is exported as a .pkl file.
* Paremeters:
  1. Input .csv file path
  2. Output .pkl file path
* Example:
```
python3 train_model.py compiled_statistics.csv model.pkl
```

### predict.py
* Loads the output model from the previous script
* Takes two player names as input, and scrapes their statistics off of the web
* Uses the model to predict the winner of the matchup, and prints either 1 for the first player winning or 2 for the second.
* Parameters:
  1. Input .pkl file
  2. First player name
  3. Second player name
* Example:
```
python3 predict.py model.pkl "Novak Djokovic" "Roger Federer"
```
