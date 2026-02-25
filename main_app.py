import streamlit as st
import requests
import numpy as np
import math
from datetime import datetime, timedelta

st.title("REAL-TIME FOOTBALL AI (Improved Match Finder)")

API_KEY = "PUT_YOUR_API_KEY_HERE"

headers = {
    "X-Auth-Token": API_KEY
}

# -------- INPUT --------
home_input = st.text_input("Home Team")
away_input = st.text_input("Away Team")

# -------- FETCH UPCOMING MATCHES --------
def get_upcoming_matches():
    today = datetime.utcnow().date()
    next_week = today + timedelta(days=7)

    url = f"https://api.football-data.org/v4/matches?dateFrom={today}&dateTo={next_week}"
    
    response = requests.get(url, headers=headers)
    return response.json().get("matches", [])

# -------- MODEL --------
def run_simulation(home_xg=1.5, away_xg=1.2):
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

    return home_win/simulations, draw/simulations, away_win/simulations

# -------- SEARCH --------
if st.button("Search Match"):

    matches = get_upcoming_matches()

    found_matches = []

    for match in matches:
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]

        if home_input.lower() in home.lower() and away_input.lower() in away.lower():
            found_matches.append(match)

    if len(found_matches) == 0:
        st.error("No match found in next 7 days.")
        st.write("Tip: Try full official team name like 'Manchester United'")
    else:
        for match in found_matches:
            st.success(f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}")
            st.write("Date:", match["utcDate"])
            st.write("League:", match["competition"]["name"])

            home_p, draw_p, away_p = run_simulation()

            st.subheader("Monte Carlo Result (10,000 runs)")
            st.write(f"Home Win: {home_p*100:.2f}%")
            st.write(f"Draw: {draw_p*100:.2f}%")
            st.write(f"Away Win: {away_p*100:.2f}%")
