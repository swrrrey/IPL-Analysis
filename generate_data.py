"""
IPL Data Generator
Generates realistic matches.csv and deliveries.csv files for the IPL dashboard.
Data structure mirrors the official Kaggle IPL dataset.
"""

import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

# ─── Constants ────────────────────────────────────────────────────────────────
TEAMS = [
    "Mumbai Indians",
    "Chennai Super Kings",
    "Royal Challengers Bengaluru",
    "Kolkata Knight Riders",
    "Rajasthan Royals",
    "Delhi Capitals",
    "Sunrisers Hyderabad",
    "Punjab Kings",
    "Lucknow Super Giants",
    "Gujarat Titans",
]

TEAM_ABBR = {
    "Mumbai Indians": "MI",
    "Chennai Super Kings": "CSK",
    "Royal Challengers Bengaluru": "RCB",
    "Kolkata Knight Riders": "KKR",
    "Rajasthan Royals": "RR",
    "Delhi Capitals": "DC",
    "Sunrisers Hyderabad": "SRH",
    "Punjab Kings": "PBKS",
    "Lucknow Super Giants": "LSG",
    "Gujarat Titans": "GT",
}

# Teams active per season
SEASON_TEAMS = {
    2008: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Rajasthan Royals","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings"],
    2009: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Rajasthan Royals","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings"],
    2010: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Rajasthan Royals","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings"],
    2011: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Rajasthan Royals","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings"],
    2012: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Rajasthan Royals","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings"],
    2013: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Rajasthan Royals","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings"],
    2014: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Rajasthan Royals","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings"],
    2015: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Rajasthan Royals","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings"],
    2016: ["Mumbai Indians","Royal Challengers Bengaluru","Kolkata Knight Riders","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings","Gujarat Titans","Rajasthan Royals"],
    2017: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings","Rajasthan Royals"],
    2018: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings","Rajasthan Royals"],
    2019: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings","Rajasthan Royals"],
    2020: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings","Rajasthan Royals"],
    2021: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings","Rajasthan Royals"],
    2022: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings","Rajasthan Royals","Lucknow Super Giants","Gujarat Titans"],
    2023: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings","Rajasthan Royals","Lucknow Super Giants","Gujarat Titans"],
    2024: ["Mumbai Indians","Chennai Super Kings","Royal Challengers Bengaluru","Kolkata Knight Riders","Delhi Capitals","Sunrisers Hyderabad","Punjab Kings","Rajasthan Royals","Lucknow Super Giants","Gujarat Titans"],
}

VENUES = [
    "Wankhede Stadium, Mumbai",
    "M Chinnaswamy Stadium, Bengaluru",
    "Eden Gardens, Kolkata",
    "MA Chidambaram Stadium, Chennai",
    "Arun Jaitley Stadium, Delhi",
    "Rajiv Gandhi International Stadium, Hyderabad",
    "Sawai Mansingh Stadium, Jaipur",
    "Punjab Cricket Association IS Bindra Stadium, Mohali",
    "Narendra Modi Stadium, Ahmedabad",
    "Ekana Cricket Stadium, Lucknow",
    "Dr DY Patil Sports Academy, Mumbai",
    "Brabourne Stadium, Mumbai",
]

TEAM_HOME_VENUE = {
    "Mumbai Indians": "Wankhede Stadium, Mumbai",
    "Chennai Super Kings": "MA Chidambaram Stadium, Chennai",
    "Royal Challengers Bengaluru": "M Chinnaswamy Stadium, Bengaluru",
    "Kolkata Knight Riders": "Eden Gardens, Kolkata",
    "Delhi Capitals": "Arun Jaitley Stadium, Delhi",
    "Sunrisers Hyderabad": "Rajiv Gandhi International Stadium, Hyderabad",
    "Rajasthan Royals": "Sawai Mansingh Stadium, Jaipur",
    "Punjab Kings": "Punjab Cricket Association IS Bindra Stadium, Mohali",
    "Gujarat Titans": "Narendra Modi Stadium, Ahmedabad",
    "Lucknow Super Giants": "Ekana Cricket Stadium, Lucknow",
}

# Realistic batters & bowlers
BATTERS = [
    "V Kohli","RG Sharma","DA Warner","AB de Villiers","MS Dhoni","SK Raina",
    "G Gambhir","SC Ganguly","SR Tendulkar","RV Uthappa","KL Rahul","S Dhawan",
    "AM Rahane","AT Rayudu","SV Samson","KA Pollard","DJ Bravo","F du Plessis",
    "SPD Smith","JC Buttler","SL Malinga","CH Gayle","A Symonds","V Sehwag",
    "SR Watson","MEK Hussey","JP Duminy","YK Pathan","PP Shaw","SA Yadav",
    "DR Sams","RA Jadeja","RP Singh","MM Sharma","A Nortje","R Ashwin",
    "IS Sodhi","T Natarajan","M Pathirana","Shubman Gill","HH Pandya",
    "DP Conway","Q de Kock","PD Salt","NM Coulter-Nile","JM Sharma",
]

BOWLERS = [
    "SL Malinga","R Ashwin","DJ Bravo","YS Chahal","Rashid Khan","B Kumar",
    "JJ Bumrah","MM Patel","PP Chawla","HH Pandya","A Nortje","T Natarajan",
    "Harbhajan Singh","Z Khan","UT Yadav","A Nehra","I Sharma","MG Johnson",
    "DW Steyn","MA Starc","JP Faulkner","KD Karthik","AS Rajpoot","M Pathirana",
    "Avesh Khan","YBK Jaiswal","M Theekshana","AR Patel","KH Pandya",
    "Washington Sundar","Arshdeep Singh","Akash Deep","Kuldeep Yadav",
]

TOSS_DECISIONS = ["bat", "field"]
WIN_BY = ["runs", "wickets"]
RESULTS = ["Normal", "D/L", "Tie", "No Result"]

# Win probability weights per team (higher = wins more)
TEAM_WIN_WEIGHTS = {
    "Mumbai Indians": 1.4,
    "Chennai Super Kings": 1.3,
    "Kolkata Knight Riders": 1.1,
    "Royal Challengers Bengaluru": 0.9,
    "Sunrisers Hyderabad": 1.0,
    "Rajasthan Royals": 1.0,
    "Delhi Capitals": 0.9,
    "Punjab Kings": 0.85,
    "Gujarat Titans": 1.1,
    "Lucknow Super Giants": 1.0,
}


def pick_winner(team1, team2):
    w1 = TEAM_WIN_WEIGHTS.get(team1, 1.0)
    w2 = TEAM_WIN_WEIGHTS.get(team2, 1.0)
    return random.choices([team1, team2], weights=[w1, w2])[0]


def generate_matches():
    matches = []
    match_id = 1

    for season in range(2008, 2025):
        teams = SEASON_TEAMS[season]
        n_teams = len(teams)
        # Each team plays every other team twice in group stage
        matchups = []
        for i in range(n_teams):
            for j in range(i + 1, n_teams):
                matchups.append((teams[i], teams[j]))
                matchups.append((teams[j], teams[i]))
        random.shuffle(matchups)

        start_date = datetime(season, 3, 22)
        for idx, (t1, t2) in enumerate(matchups):
            match_date = start_date + timedelta(days=idx // 2)
            venue = TEAM_HOME_VENUE.get(t1, random.choice(VENUES))
            toss_winner = random.choice([t1, t2])
            toss_decision = random.choice(TOSS_DECISIONS)
            winner = pick_winner(t1, t2)
            result = random.choices(RESULTS, weights=[88, 4, 4, 4])[0]
            if result == "Normal":
                win_by = random.choice(WIN_BY)
                if win_by == "runs":
                    margin = random.randint(1, 120)
                else:
                    margin = random.randint(1, 10)
            else:
                win_by = None
                margin = None
                winner = None

            player_of_match = random.choice(BATTERS + BOWLERS)

            matches.append({
                "id": match_id,
                "season": season,
                "city": venue.split(",")[-1].strip(),
                "date": match_date.strftime("%Y-%m-%d"),
                "team1": t1,
                "team2": t2,
                "toss_winner": toss_winner,
                "toss_decision": toss_decision,
                "result": result,
                "dl_applied": 1 if result == "D/L" else 0,
                "winner": winner,
                "win_by_runs": margin if win_by == "runs" else 0,
                "win_by_wickets": margin if win_by == "wickets" else 0,
                "player_of_match": player_of_match,
                "venue": venue,
                "umpire1": "Umpire A",
                "umpire2": "Umpire B",
            })
            match_id += 1

    return pd.DataFrame(matches)


def generate_deliveries(matches_df):
    deliveries = []
    total = len(matches_df)
    print(f"Generating deliveries for {total} matches...")

    for idx, row in matches_df.iterrows():
        match_id = row["id"]
        team1 = row["team1"]
        team2 = row["team2"]
        if idx % 200 == 0:
            print(f"  Processing match {idx}/{total}...")

        # Each innings: batting team scores
        for inning in [1, 2]:
            batting_team = team1 if inning == 1 else team2
            bowling_team = team2 if inning == 1 else team1

            # Pick random batters & bowlers from generic pool
            bat_lineup = random.sample(BATTERS, min(11, len(BATTERS)))
            bowl_lineup = random.sample(BOWLERS, min(8, len(BOWLERS)))

            over = 0
            ball_in_over = 1
            total_balls = 0
            wickets = 0
            batter_idx = 0
            current_batter = bat_lineup[0]
            non_striker = bat_lineup[1]
            batter_idx = 2

            for over in range(20):
                bowler = bowl_lineup[over % len(bowl_lineup)]
                ball_in_over = 1
                legal_balls = 0

                while legal_balls < 6:
                    is_wide = random.random() < 0.04
                    is_no_ball = random.random() < 0.02
                    is_extra = is_wide or is_no_ball
                    batter_runs = 0 if is_wide else random.choices(
                        [0, 1, 2, 3, 4, 6],
                        weights=[40, 25, 8, 2, 15, 10]
                    )[0]
                    extra_runs = 1 if is_extra else 0
                    total_runs = batter_runs + extra_runs

                    is_wicket = False
                    dismissal_kind = None
                    player_dismissed = None
                    fielder = None

                    if not is_wide and not is_no_ball and wickets < 10:
                        if random.random() < 0.065:
                            is_wicket = True
                            wickets += 1
                            dismissal_kind = random.choice(
                                ["caught", "bowled", "lbw", "run out", "stumped", "caught and bowled"]
                            )
                            player_dismissed = current_batter
                            if dismissal_kind in ["caught", "run out", "stumped"]:
                                fielder = random.choice(bowl_lineup)
                            if batter_idx < len(bat_lineup):
                                current_batter = bat_lineup[batter_idx]
                                batter_idx += 1

                    deliveries.append({
                        "match_id": match_id,
                        "inning": inning,
                        "batting_team": batting_team,
                        "bowling_team": bowling_team,
                        "over": over + 1,
                        "ball": ball_in_over,
                        "batter": current_batter,
                        "bowler": bowler,
                        "non_striker": non_striker,
                        "batsman_runs": batter_runs,
                        "extra_runs": extra_runs,
                        "total_runs": total_runs,
                        "extras_type": "wides" if is_wide else ("noballs" if is_no_ball else None),
                        "is_wicket": 1 if is_wicket else 0,
                        "player_dismissed": player_dismissed,
                        "dismissal_kind": dismissal_kind,
                        "fielder": fielder,
                    })

                    if not is_wide and not is_no_ball:
                        legal_balls += 1
                        ball_in_over += 1
                        if batter_runs % 2 == 1:
                            current_batter, non_striker = non_striker, current_batter

                    total_balls += 1
                    if wickets >= 10:
                        break

                if wickets >= 10:
                    break

    return pd.DataFrame(deliveries)


def main():
    os.makedirs("data", exist_ok=True)

    print("Generating matches data...")
    matches_df = generate_matches()
    matches_df.to_csv("data/matches.csv", index=False)
    print(f"matches.csv saved - {len(matches_df)} rows")

    print("Generating deliveries data (this may take ~1 min)...")
    deliveries_df = generate_deliveries(matches_df)
    deliveries_df.to_csv("data/deliveries.csv", index=False)
    print(f"deliveries.csv saved - {len(deliveries_df)} rows")
    print("\nDone! Data is ready in the 'data/' folder.")


if __name__ == "__main__":
    main()
