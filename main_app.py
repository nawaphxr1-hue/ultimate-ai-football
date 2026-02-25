import streamlit as st
import requests
import numpy as np
import math
from datetime import datetime, timedelta
from difflib import SequenceMatcher

st.title("SMART REAL-TIME FOOTBALL AI")

API_KEY = "PUT_YOUR_API_KEY_HERE"

headers = {"X-Auth-Token": API_KEY}

home_input = st.text_input("Home Team")
away_input = st.text_input("Away Team")

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def get_matches():
    today = datetime.utcnow().date()
    future = today + timedelta(days=30)

    url = f"https://api.football-data.org/v4/matches?dateFrom={today}&dateTo={future}"
    r = requests.get(url, headers=headers)
    return r.json().get("matches", [])

if st.button("Search Match"):

    matches = get_matches()
    found = []

    for match in matches:
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]

        if similarity(home_input, home) > 0.6 and similarity(away_input, away) > 0.6:
            found.append(match)

    if not found:
        st.error("No match found in next 30 days.")
        st.write("Check spelling. Example: Borussia Dortmund")
    else:
        for match in found:
            st.success(f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}")
            st.write("Date:", match["utcDate"])
            st.write("League:", match["competition"]["name"])

            # Monte Carlo
            simulations = 10000
            home_xg = 1.5
            away_xg = 1.2

            home_win = draw = away_win = 0

            for _ in range(simulations):
                h = np.random.poisson(home_xg)
                a = np.random.poisson(away_xg)

                if h > a:
                    home_win += 1
                elif h == a:
                    draw += 1
                else:
                    away_win += 1

            st.subheader("AI Simulation")
            st.write(f"Home Win: {home_win/simulations*100:.2f}%")
            st.write(f"Draw: {draw/simulations*100:.2f}%")
            st.write(f"Away Win: {away_win/simulations*100:.2f}%")
