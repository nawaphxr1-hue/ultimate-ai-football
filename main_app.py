import streamlit as st
import requests
from datetime import datetime, timedelta

st.title("PRO TEAM MATCH FINDER")

API_KEY = "PUT_YOUR_API_KEY_HERE"
headers = {"X-Auth-Token": API_KEY}

home_input = st.text_input("Home Team")
away_input = st.text_input("Away Team")

# ---------- GET TEAM ID ----------
def get_team_id(team_name):
    url = f"https://api.football-data.org/v4/teams"
    r = requests.get(url, headers=headers)
    teams = r.json().get("teams", [])

    for team in teams:
        if team_name.lower() in team["name"].lower():
            return team["id"]

    return None

# ---------- GET MATCHES FOR TEAM ----------
def get_team_matches(team_id):
    today = datetime.utcnow().date()
    future = today + timedelta(days=60)

    url = f"https://api.football-data.org/v4/teams/{team_id}/matches?dateFrom={today}&dateTo={future}"
    r = requests.get(url, headers=headers)
    return r.json().get("matches", [])

if st.button("Search Match"):

    home_id = get_team_id(home_input)
    away_id = get_team_id(away_input)

    if not home_id or not away_id:
        st.error("Team not found in API database.")
    else:
        home_matches = get_team_matches(home_id)

        found = []

        for match in home_matches:
            if match["awayTeam"]["id"] == away_id:
                found.append(match)

        if not found:
            st.error("No upcoming match found between these teams in next 60 days.")
        else:
            for match in found:
                st.success(f"{match['homeTeam']['name']} vs {match['awayTeam']['name']}")
                st.write("Date:", match["utcDate"])
                st.write("Competition:", match["competition"]["name"])
