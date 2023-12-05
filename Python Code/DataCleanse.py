from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.endpoints import teamdashboardbygeneralsplits

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

        # Separate columns of interest
        columns = ['TEAM_GAME_LOCATION', 'W', 'L', 'FG_PCT_RANK', 'FG3_PCT_RANK', 'FT_PCT_RANK', 
                'OREB_RANK', 'DREB_RANK', 'REB_RANK', 'AST_RANK', 'TOV_RANK', ]
        advanced_team_stats = advanced_team_stats[columns]

        # Append to dictionary
        teamStatsDict[row['TEAM_NAME']] = advanced_team_stats

    return teamStatsDict