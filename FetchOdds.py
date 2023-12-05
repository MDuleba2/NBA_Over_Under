import argparse
import requests
import json
from datetime import datetime, timedelta

# Obtain the API key that was passed in from the command line
parser = argparse.ArgumentParser(description='Sample V4')
parser.add_argument('--api-key', type=str, default='')
args = parser.parse_args()

# API key
API_KEY = '646b0393ded79e0cd0c697223dc626d2'

# Parameters of interest
SPORT = 'basketball_nba'
REGIONS = 'us' 
MARKETS = 'totals' 
ODDS_FORMAT = 'decimal' 
DATE_FORMAT = 'iso' 

# Request
sports_response = requests.get('https://api.the-odds-api.com/v4/sports', params={
    'api_key': API_KEY
})

# Handle request
if sports_response.status_code != 200:
    print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')
else:
    sports_data = sports_response.json()
    with open('sports_data.json', 'w') as sports_file:
        json.dump(sports_data, sports_file, indent=4)

# Fetch odds
odds_response = requests.get(f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds', params={
    'api_key': API_KEY,
    'regions': REGIONS,
    'markets': MARKETS,
    'oddsFormat': ODDS_FORMAT,
    'dateFormat': DATE_FORMAT,
})

# Get todays date
today_date = datetime.utcnow().date()

# Handle fetch
if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
else:
    # Convert the response to a list
    odds_data = odds_response.json()  
    # Create filtered data 
    fanDuel_data = []

    # Filter data to desired sports book
    for game in odds_data:

        game_date = datetime.strptime(game['commence_time'], '%Y-%m-%dT%H:%M:%SZ').date()
        if game_date == today_date:
            for bookmaker in game['bookmakers']:
                if bookmaker['title'] == 'FanDuel':
                    fanDuel_data.append({
                        'id': game['id'],
                        'sport_key': game['sport_key'],
                        'sport_title': game['sport_title'],
                        'commence_time': game['commence_time'],
                        'home_team': game['home_team'],
                        'away_team': game['away_team'],
                        'bookmaker': bookmaker
                    })

    # Display the filtered data
    with open('NBA_OverUnder.json', 'w') as file:
        json.dump(fanDuel_data, file, indent=4)

    # Display remaining requests
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])