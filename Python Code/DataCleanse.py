from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.endpoints import teamdashboardbygeneralsplits
import pandas as pd

def getTeamStats(season):
    '''
    Method that returns a df with every NBA team
    name along with their respective team stats and 
    advanced analytics
    
    @param season: the desired season
    @return team_stats_df
    '''

    # Fetching team stats for the current season
    team_stats_df = leaguedashteamstats.LeagueDashTeamStats(season=season).get_data_frames()[0]
    team_stats_df['TEAM_NAME'] = team_stats_df['TEAM_NAME'].replace('LA Clippers', 'Los Angeles Clippers')

    # Set index as the team name
    team_stats_df.index = team_stats_df['TEAM_NAME']

    # Columns of interest
    columns_of_interest = ['FG_PCT_RANK', 'FG3_PCT_RANK', 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 'REB_RANK',
                           'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 'PTS_RANK']
    
    # Filter out unnecessary columns
    team_stats_df = team_stats_df.filter(items=columns_of_interest)

    return team_stats_df