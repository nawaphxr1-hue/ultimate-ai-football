import requests
import numpy as np
import pandas as pd
from scipy.stats import poisson
from datetime import datetime
from tabulate import tabulate

# -----------------------------
# ⚙️ ตั้งค่า
# -----------------------------
HOME_ADVANTAGE = 1.10   # บวก 10% ให้ทีมเหย้า
MAX_GOALS = 6


# -----------------------------
# 1️⃣ ดึงโปรแกรมวันนี้จาก FotMob
# -----------------------------
def get_today_matches():
    today = datetime.now().strftime("%Y%m%d")
    url = f"https://www.fotmob.com/api/matches?date={today}"
    data = requests.get(url).json()
    
    matches = []
    
    for league in data.get("leagues", []):
        for match in league.get("matches", []):
            if match.get("status", {}).get("finished") is False:
                home = match["home"]["name"]
                away = match["away"]["name"]
                matches.append((home, away))
    
    return matches


# -----------------------------
# 2️⃣ ค้นหา Team ID
# -----------------------------
def get_team_id(team_name):
    url = f"https://www.fotmob.com/api/search?term={team_name}"
    res = requests.get(url).json()
    
    for item in res.get("teams", []):
        if team_name.lower() in item["name"].lower():
            return item["id"]
    return None


# -----------------------------
# 3️⃣ ดึงค่า xG ล่าสุด
# -----------------------------
def get_team_xg(team_id):
    url = f"https://www.fotmob.com/api/teams?id={team_id}"
    data = requests.get(url).json()
    
    matches = data.get("recentMatches", [])
    xg_list = []
    
    for m in matches[:5]:
        if "xg" in m:
            xg_list.append(m["xg"])
    
    if len(xg_list) > 0:
        return np.mean(xg_list)
    else:
        return 1.2


# -----------------------------
# 4️⃣ Poisson Model
# -----------------------------
def predict(home_xg, away_xg):
    home_xg *= HOME_ADVANTAGE
    
    home_win = 0
    draw = 0
    away_win = 0
    
    for i in range(MAX_GOALS):
        for j in range(MAX_GOALS):
            prob = poisson.pmf(i, home_xg) * poisson.pmf(j, away_xg)
            if i > j:
                home_win += prob
            elif i == j:
                draw += prob
            else:
                away_win += prob
    
    return round(home_win*100,2), round(draw*100,2), round(away_win*100,2)


# -----------------------------
# 🔥 วิเคราะห์ทั้งหมดวันนี้
# -----------------------------
def analyze_today():
    matches = get_today_matches()
    
    if not matches:
        print("ไม่มีแมตช์วันนี้")
        return
    
    results = []
    
    for home, away in matches:
        print(f"กำลังวิเคราะห์ {home} vs {away}")
        
        home_id = get_team_id(home)
        away_id = get_team_id(away)
        
        if home_id and away_id:
            home_xg = get_team_xg(home_id)
            away_xg = get_team_xg(away_id)
            
            h, d, a = predict(home_xg, away_xg)
            
            results.append([home, away, h, d, a])
        else:
            results.append([home, away, "Error", "Error", "Error"])
    
    df = pd.DataFrame(results, columns=[
        "Home Team", "Away Team", 
        "Home Win %", "Draw %", "Away Win %"
    ])
    
    print("\n📊 ผลวิเคราะห์วันนี้")
    print(tabulate(df, headers="keys", tablefmt="pretty"))
    
    df.to_excel("today_match_analysis.xlsx", index=False)
    print("\n📁 Export ไฟล์แล้ว: today_match_analysis.xlsx")


# -----------------------------
# ▶️ RUN
# -----------------------------
analyze_today()
