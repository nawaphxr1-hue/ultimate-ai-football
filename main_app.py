import streamlit as st
import requests
import numpy as np
import math

st.set_page_config(layout="wide")
st.title("FULL AUTO REAL-TIME FOOTBALL AI (Manual Team Input)")

API_KEY = "PUT_YOUR_API_KEY_HERE"

headers = {
    "X-Auth-Token": API_KEY
}

# ---------------- USER INPUT ----------------

home_team_input = st.text_input("Enter Home Team Name")
away_team_input = st.text_input("Enter Away Team Name")

# ---------------- SEARCH MATCH ----------------

def find_match(home_name, away_name):
    response = requests.get(
        "https://api.football-data.org/v4/matches",
        headers=headers
    )
    
    data = response.json()
    matches = data.get("matches", [])

    for match in matches:
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]

        if home_name.lower() in home.lower() and away_name.lower() in away.lower():
            return match

    return None

# ---------------- MODEL ----------------

def poisson(lam, k):
    return (lam**k * math.exp(-lam)) / math.factorial(k)

if st.button("Search & Run AI"):

    match = find_match(home_team_input, away_team_input)

    if match is None:
        st.error("Match not found in upcoming fixtures.")
    else:
        st.success("Match Found!")

        st.write("Date:", match["utcDate"])
        st.write("League:", match["competition"]["name"])

        # -------- Baseline Model (สามารถต่อยอดดึงสถิติจริงได้) --------
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

        st.subheader("Monte Carlo Simulation (10,000 runs)")
        st.write(f"Home Win: {home_win/simulations*100:.2f}%")
        st.write(f"Draw: {draw/simulations*100:.2f}%")
        st.write(f"Away Win: {away_win/simulations*100:.2f}%")
