import streamlit as st
import requests
from PIL import Image
from datetime import datetime

# ===============================
# CONFIG
# ===============================
API_KEY = "YOUR_API_KEY"
BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}

st.set_page_config(page_title="PRO TEAM MATCH FINDER", layout="wide")

st.title("⚽ PRO TEAM MATCH FINDER - FULL VERSION")

# ===============================
# IMAGE UPLOAD SECTION
# ===============================
st.subheader("📷 Upload Custom Team Images (Optional)")

col1, col2 = st.columns(2)

with col1:
    home_custom_img = st.file_uploader("Upload Home Team Image", type=["png", "jpg", "jpeg"])

with col2:
    away_custom_img = st.file_uploader("Upload Away Team Image", type=["png", "jpg", "jpeg"])

# ===============================
# TEAM SEARCH
# ===============================
st.subheader("🔎 Search Teams")

home_team = st.text_input("Home Team Name")
away_team = st.text_input("Away Team Name")


def get_team_data(team_name):
    url = f"{BASE_URL}/teams"
    params = {"search": team_name}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if data["response"]:
        team = data["response"][0]["team"]
        return team["id"], team["name"], team["logo"]
    return None, None, None


def get_h2h(home_id, away_id):
    url = f"{BASE_URL}/fixtures/headtohead"
    params = {
        "h2h": f"{home_id}-{away_id}",
        "last": 5
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()


# ===============================
# BUTTON ACTION
# ===============================
if st.button("🔥 Find Match"):

    home_id, home_name, home_logo = get_team_data(home_team)
    away_id, away_name, away_logo = get_team_data(away_team)

    if not home_id or not away_id:
        st.error("❌ Team not found in API database.")
    else:
        st.success("✅ Teams Found!")

        # ===============================
        # SHOW TEAM INFO
        # ===============================
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### 🏠 {home_name}")
            if home_custom_img:
                st.image(home_custom_img, use_container_width=True)
            else:
                st.image(home_logo, width=150)

        with col2:
            st.markdown(f"### ✈️ {away_name}")
            if away_custom_img:
                st.image(away_custom_img, use_container_width=True)
            else:
                st.image(away_logo, width=150)

        # ===============================
        # H2H DATA
        # ===============================
        st.subheader("📊 Last 5 Head-to-Head Matches")

        h2h_data = get_h2h(home_id, away_id)

        if h2h_data["response"]:
            for match in h2h_data["response"]:
                date = datetime.strptime(match["fixture"]["date"], "%Y-%m-%dT%H:%M:%S%z")
                league = match["league"]["name"]
                home = match["teams"]["home"]["name"]
                away = match["teams"]["away"]["name"]
                goals_home = match["goals"]["home"]
                goals_away = match["goals"]["away"]

                st.markdown(
                    f"""
                    **{date.strftime('%d %B %Y')}**  
                    🏆 {league}  
                    ⚽ {home} {goals_home} - {goals_away} {away}
                    ---
                    """
                )
        else:
            st.warning("No recent matches found between these teams.")
