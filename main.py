import requests
import datetime
import csv

# Dictionary to map team names to their three-letter abbreviations
team_abbreviations = {
    "Arizona Diamondbacks": "ARI",
    "Atlanta Braves": "ATL",
    "Baltimore Orioles": "BAL",
    "Boston Red Sox": "BOS",
    "Chicago White Sox": "CWS",
    "Chicago Cubs": "CHC",
    "Cincinnati Reds": "CIN",
    "Cleveland Guardians": "CLE",
    "Colorado Rockies": "COL",
    "Detroit Tigers": "DET",
    "Houston Astros": "HOU",
    "Kansas City Royals": "KC",
    "Los Angeles Angels": "LAA",
    "Los Angeles Dodgers": "LAD",
    "Miami Marlins": "MIA",
    "Milwaukee Brewers": "MIL",
    "Minnesota Twins": "MIN",
    "New York Yankees": "NYY",
    "New York Mets": "NYM",
    "Oakland Athletics": "OAK",
    "Philadelphia Phillies": "PHI",
    "Pittsburgh Pirates": "PIT",
    "San Diego Padres": "SD",
    "San Francisco Giants": "SF",
    "Seattle Mariners": "SEA",
    "St. Louis Cardinals": "STL",
    "Tampa Bay Rays": "TB",
    "Texas Rangers": "TEX",
    "Toronto Blue Jays": "TOR",
    "Washington Nationals": "WSH",
}

# Get yesterday's date in the required format
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

# API URL with the date
url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={yesterday}"

# Fetch data from the API
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    game_results = []

    # Extract the required fields
    for date in data.get("dates", []):
        for game in date.get("games", []):
            home_team_name = game["teams"]["home"]["team"]["name"]
            away_team_name = game["teams"]["away"]["team"]["name"]
            game_info = {
                "home_team": team_abbreviations.get(home_team_name, home_team_name),
                "away_team": team_abbreviations.get(away_team_name, away_team_name),
                "home_team_score": game["teams"]["home"].get("score", "N/A"),
                "away_team_score": game["teams"]["away"].get("score", "N/A"),
            }
            game_results.append(game_info)

    # Save the extracted data to a CSV file
    with open(f"data/mlb_game_results_{yesterday}.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["home_team", "away_team", "home_team_score", "away_team_score"],
        )
        writer.writeheader()
        writer.writerows(game_results)

    print(f"Game results for {yesterday} have been fetched and saved.")
else:
    print(f"Failed to fetch data: {response.status_code}")
