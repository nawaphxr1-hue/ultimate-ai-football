import numpy as np
from scipy.stats import poisson

def elo_probability(home_elo, away_elo):
    return 1 / (1 + 10 ** ((away_elo - home_elo) / 400))

def expected_goals_model(
    home_xg, away_xg,
    home_avg_scored, home_avg_conceded,
    away_avg_scored, away_avg_conceded,
    home_shots_on_target, away_shots_on_target,
    home_form, away_form,
    home_elo, away_elo,
    h2h_home_win_rate
):
    # Base Expected Goals
    home_lambda = (
        home_xg * 0.4 +
        home_avg_scored * 0.2 +
        away_avg_conceded * 0.2 +
        home_shots_on_target * 0.05 +
        (home_form - away_form) * 0.03 +
        h2h_home_win_rate * 0.1
    )

    away_lambda = (
        away_xg * 0.4 +
        away_avg_scored * 0.2 +
        home_avg_conceded * 0.2 +
        away_shots_on_target * 0.05 +
        (away_form - home_form) * 0.03
    )

    # Elo adjustment
    elo_prob = elo_probability(home_elo, away_elo)
    home_lambda += elo_prob * 0.3
    away_lambda += (1 - elo_prob) * 0.3

    # Home advantage
    home_lambda += 0.25

    return max(home_lambda, 0.2), max(away_lambda, 0.2)


def monte_carlo_simulation(home_lambda, away_lambda, simulations=10000, handicap=-0.5, ou_line=2.5):
    home_win = 0
    draw = 0
    away_win = 0
    handicap_cover = 0
    over = 0

    for _ in range(simulations):
        home_goals = np.random.poisson(home_lambda)
        away_goals = np.random.poisson(away_lambda)

        # Result
        if home_goals > away_goals:
            home_win += 1
        elif home_goals == away_goals:
            draw += 1
        else:
            away_win += 1

        # Handicap
        if (home_goals - away_goals) > abs(handicap):
            handicap_cover += 1

        # Over/Under
        if (home_goals + away_goals) > ou_line:
            over += 1

    return {
        "Home Win %": round(home_win / simulations * 100, 2),
        "Draw %": round(draw / simulations * 100, 2),
        "Away Win %": round(away_win / simulations * 100, 2),
        "Home Cover Handicap %": round(handicap_cover / simulations * 100, 2),
        "Over {} %".format(ou_line): round(over / simulations * 100, 2)
    }


def analyze_pro_match(data):
    home_lambda, away_lambda = expected_goals_model(**data)

    result = monte_carlo_simulation(
        home_lambda,
        away_lambda,
        simulations=10000,
        handicap=data.get("handicap", -0.5),
        ou_line=data.get("ou_line", 2.5)
    )

    print("Expected Goals:")
    print("Home xG:", round(home_lambda, 2))
    print("Away xG:", round(away_lambda, 2))
    print("\nProbability Result:")
    for k, v in result.items():
        print(k, ":", v, "%")


# ======================
# 🔢 ตัวอย่างใส่ข้อมูลจริง
# ======================

match_data = {
    "home_xg": 1.8,
    "away_xg": 1.2,
    "home_avg_scored": 1.7,
    "home_avg_conceded": 1.0,
    "away_avg_scored": 1.1,
    "away_avg_conceded": 1.5,
    "home_shots_on_target": 5.5,
    "away_shots_on_target": 4.0,
    "home_form": 10,  # 5 นัดล่าสุด
    "away_form": 6,
    "home_elo": 1750,
    "away_elo": 1650,
    "h2h_home_win_rate": 0.6,
    "handicap": -0.5,
    "ou_line": 2.5
}

analyze_pro_match(match_data)
