import streamlit as st
import requests

API_KEY = "YOUR_API_KEY"
BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}

st.title("PRO TEAM MATCH FINDER")

home_team = st.text_input("Home Team")
away_team = st.text_input("Away Team")

def get_team_id(team_name):
    url = f"{BASE_URL}/teams"
    params = {"search": team_name}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if data["response"]:
        return data["response"][0]["team"]["id"]
    else:
        return None

if st.button("Search Match"):
    home_id = get_team_id(home_team)
    away_id = get_team_id(away_team)

    if not home_id or not away_id:
        st.error("Team not found in API database.")
    else:
        st.success(f"Found Teams! Home ID: {home_id} | Away ID: {away_id}")
      import streamlit as st
from PIL import Image

st.title("PRO TEAM MATCH FINDER")

# 🔽 อัปโหลดรูป
uploaded_file = st.file_uploader("Upload Team Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)
