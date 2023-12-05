from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.endpoints import teamdashboardbygeneralsplits
import pandas as pd
import json

# Path to file containing todays over/unders
slate_path = r'NBA_OverUnder.json'

# Seasons
previousSeason = '2022-23'
currentSeason = '2023-24'

def getStatsDict(season):
    '''
    Method that returns a dict with every NBA team
    name along with their respective team stats and 
    advanced analytics
    
    @param season: the desired season
    @return teamStatsDict
    '''

    # Declare dictionary to hold all stats
    teamStatsDict = {}
    
    # Fetching team stats for the current season
    team_stats = leaguedashteamstats.LeagueDashTeamStats(season=season).get_data_frames()[0]
    
    # Loop through each team in original df
    for index, row in team_stats.iterrows():
        # Extract team and advanaced stats for each team
        advanced_team_stats = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=row['TEAM_ID'], season=season, season_type_all_star='Regular Season').get_data_frames()[1]

        # Append to dictionary
        teamStatsDict[row['TEAM_NAME']] = advanced_team_stats

    return teamStatsDict

def getSlateDict(filePath):
    '''
    Method to get the games that are being played today with
    the home and away teams along with the total points.

    @param filePath: path to JSON file
    @return slateDict
    '''

    # Open JSON
    with open(filePath, 'r') as file:
        json_data = json.load(file)

    # Create dict
    slateDict = {}
    
    # Loop through games
    for index, game in enumerate(json_data, start=1):
        home_team = game['home_team']
        away_team = game['away_team']
        point_total = None
        
        for outcome in game['bookmaker']['markets'][0]['outcomes']:
            if outcome['name'] == 'Over':
                point_total = outcome['point']
                break
        
        # Store game info
        slateDict[f"Game {index}"] = {'home': home_team, 'away': away_team, 'total': point_total}
    
    return slateDict

def filterTeamStats(slateDict : dict, teamStatsDict : dict):
    '''
    Narrow down original team stats dictionary to 
    teams that are only playing in todays games.
    
    @param slateDict: dict containing gamne info
    @param teamStatsDict: orginal dictionary
    @return today_dict
    '''
    
    # Extract teams playing today
    teams = set()
    for game_details in slateDict.values():
        teams.add(game_details['home'])
        teams.add(game_details['away'])

    # Filter teams playing today
    today_dict = {team: teamStatsDict[team] for team in teams}

    return today_dict

def main():
    
    previous_team_stats = getStatsDict(previousSeason)
    current_team_stats = getStatsDict(currentSeason)
    slate_dict = getSlateDict(slate_path)
    today_dict = filterTeamStats(slate_dict, current_team_stats)

    return today_dict