import sys
from sklearn import linear_model, svm
import pandas as pd
import joblib

def clean_dataset(df):
    df = df.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna(axis=1)
    return df

input_filename = sys.argv[1]
dataset = pd.read_csv(input_filename)
clean_dataset = clean_dataset(dataset)

X = clean_dataset[['p1_matches_played', 'p2_matches_played', 'p1_balanced_leverage_ratio', 'p2_balanced_leverage_ratio', 'p1_dominance_ratio_plus', 'p2_dominance_ratio_plus', 'p1_excitement_index', 'p2_excitement_index', 'p1_comeback_factor', 'p2_comeback_factor', 'p1_deuce_ace_percentage', 'p2_deuce_ace_percentage', 'p1_deuce_service_point_won_percentage', 'p2_deuce_service_point_won_percentage', 'p1_ad_ace_percentage', 'p2_ad_ace_percentage', 'p1_ad_service_point_won_percentage', 'p2_ad_service_point_won_percentage', 'p1_deuce_return_point_won_percentage', 'p2_deuce_return_point_won_percentage', 'p1_ad_return_point_won_percentage', 'p2_ad_return_point_won_percentage']]

y = clean_dataset['winner']

clf = svm.SVC(gamma=0.001, C=100)
clf.fit(X, y)

# save trained model to file
joblib.dump(clf, sys.argv[2])
