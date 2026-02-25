import streamlit as st
import numpy as np
import math

st.title("Ultimate AI Football Predictor V2")

home_xg = st.number_input("Home xG", value=1.5)
away_xg = st.number_input("Away xG", value=1.0)

def poisson(lam, k):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

if st.button("Predict"):

    max_goals = 5
    matrix = np.zeros((max_goals+1, max_goals+1))

    for i in range(max_goals+1):
        for j in range(max_goals+1):
            matrix[i][j] = poisson(home_xg, i) * poisson(away_xg, j)

    home_win = 0
    draw = 0
    away_win = 0

    for i in range(max_goals+1):
        for j in range(max_goals+1):
            if i > j:
                home_win += matrix[i][j]
            elif i == j:
                draw += matrix[i][j]
            else:
                away_win += matrix[i][j]

    st.subheader("Match Probabilities")
    st.write(f"Home Win: {home_win*100:.2f}%")
    st.write(f"Draw: {draw*100:.2f}%")
    st.write(f"Away Win: {away_win*100:.2f}%")

    best_score = np.unravel_index(matrix.argmax(), matrix.shape)
    st.subheader("Most Likely Score")
    st.write(f"{best_score[0]} - {best_score[1]}")
