from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.endpoints import teamdashboardbygeneralsplits
import pandas as pd


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
    team_stats = leaguedashteamstats.LeagueDashTeamStats().get_data_frames()[0]
    
    # Loop through each team in original df
    for index, row in team_stats.iterrows():
        # Extract team and advanaced stats for each team
        advanced_team_stats = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(team_id=row['TEAM_ID'], season=season, season_type_all_star='Regular Season').get_data_frames()[1]
        current_team_stats = team_stats.loc[team_stats['TEAM_ID'] == row['TEAM_ID']]

        # Append to dictionary
        teamStatsDict[row['TEAM_NAME']] = {'Team Stats': current_team_stats, 'Advanced Stats': advanced_team_stats}

    

getStatsDict('2023-24')

