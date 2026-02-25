# elo.py
def update_elo(home_elo, away_elo, result, k=20):
    expected_home = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))

    if result == "H":
        score_home = 1
    elif result == "D":
        score_home = 0.5
    else:
        score_home = 0

    new_home = home_elo + k * (score_home - expected_home)
    new_away = away_elo + k * ((1-score_home) - (1-expected_home))

    return new_home, new_away
  # features.py
import pandas as pd

def create_features(df):
    df["goal_diff"] = df["home_goals"] - df["away_goals"]
    df["elo_diff"] = df["home_elo"] - df["away_elo"]

    df["home_xg_rolling"] = df["home_xg"].rolling(5).mean()
    df["away_xg_rolling"] = df["away_xg"].rolling(5).mean()

    df["rest_diff"] = df["home_rest_days"] - df["away_rest_days"]

    return df.dropna()
  # simulation.py
import numpy as np

def monte_carlo(home_lambda, away_lambda, sims=50000):
    home_win=draw=away_win=0

    for _ in range(sims):
        h=np.random.poisson(home_lambda)
        a=np.random.poisson(away_lambda)

        if h>a: home_win+=1
        elif h==a: draw+=1
        else: away_win+=1

    return {
        "home_win%": home_win/sims*100,
        "draw%": draw/sims*100,
        "away_win%": away_win/sims*100
    }
  # ml_model.py
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier

def train_models(X,y):

    xgb = XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05
    )
    xgb.fit(X,y)

    nn = MLPClassifier(
        hidden_layer_sizes=(64,32),
        max_iter=500
    )
    nn.fit(X,y)

    return xgb, nn
  def ensemble_predict(xgb, nn, features):
    p1 = xgb.predict_proba([features])[0][1]
    p2 = nn.predict_proba([features])[0][1]

    final_prob = (p1*0.6 + p2*0.4)
    return final_prob
    # backtest.py
def evaluate_accuracy(predictions, actual):
    correct = sum((p>0.5)==a for p,a in zip(predictions,actual))
    return correct/len(actual)
  # app.py
import streamlit as st

st.title("Ultimate AI Football Predictor")

home_lambda = st.number_input("Home Expected Goals",1.5)
away_lambda = st.number_input("Away Expected Goals",1.0)

if st.button("Predict"):
    result = monte_carlo(home_lambda, away_lambda)
    st.write(result)
  streamlit run app.py
