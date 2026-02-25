import streamlit as st
import requests
import numpy as np
import math
import pandas as pd

st.set_page_config(layout="wide")
st.title("FULL AUTO REAL-TIME FOOTBALL AI")

API_KEY = "PUT_YOUR_API_KEY_HERE"

headers = {
    "X-Auth-Token": API_KEY
}

# ---------------- FETCH MATCHES ----------------

st.subheader("Upcoming Matches")

response = requests.get(
    "https://api.football-data.org/v4/matches",
    headers=headers
)

data = response.json()

matches = data.get("matches", [])

match_options = []

for match in matches[:20]:
    home = match["homeTeam"]["name"]
    away = match["awayTeam"]["name"]
    date = match["utcDate"]
    match_options.append(f"{home} vs {away} | {date}")

selected = st.selectbox("Select Match", match_options)

# ---------------- SIMPLE MODEL ----------------

def poisson(lam, k):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

if st.button("Run AI Prediction"):

    # Dummy baseline until you connect deeper stats endpoint
    home_xg = 1.5
    away_xg = 1.2

    simulations = 10000

    home_win = 0
    draw = 0
    away_win = 0

    for _ in range(simulations):
        h = np.random.poisson(home_xg)
        a = np.random.poisson(away_xg)

        if h > a:
            home_win += 1
        elif h == a:
            draw += 1
        else:
            away_win += 1

    st.subheader("AI Simulation Result (10,000 Runs)")
    st.write(f"Home Win: {home_win/simulations*100:.2f}%")
    st.write(f"Draw: {draw/simulations*100:.2f}%")
    st.write(f"Away Win: {away_win/simulations*100:.2f}%")
