import argparse
import requests
import json

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

# Handle fetch
if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')
else:
    odds_data = odds_response.json()  # Convert the response to a list

    games = []
    for data in odds_data:
        for event in data.get('data', []):
            sites = event.get('sites', [])
            for site in sites:
                if site['site_key'] == 'fanduel':
                    game_info = {
                        'home_team': event['home_team'],
                        'away_team': event['away_team'],
                        'over_under': site['odds']['totals'][0]['points']
                    }
                    games.append(game_info)
                    break  # Once found for FanDuel, break to the next event

    with open('NBA_OverUnder.json', 'w') as file:
        json.dump(games, file, indent=4)

    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])