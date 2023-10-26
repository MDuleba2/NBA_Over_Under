import pandas as pd
import requests
import bs4 as BeautifulSoup
import nba_api as nba

def getTeamDict(file_path):
    '''
    Function that creates a dict for each NBA team
    and their abbreviation.
    @param file_path: file containing list of teams and abbr
    @return dict
    '''

    # open file
    file = open(file_path)

    # loop through lines and add to dict
    teamDict = {}
    for line in file.readlines():
        lineSplit = line.split('-')

        team = lineSplit[1]

        teamDict[team[:-1]] = {'Traditional': None, 'Advanced': None}
    
    return teamDict

def getTraditionalStats(url):
    '''
    Create a dataframe for each NBA team's traditonal season stats
    @param url: url for source of stats
    @return df_traditional
    '''

    # URL for Traditional Stats
    url_traditional = url
    response_traditional = requests.get(url_traditional)
    soup_traditional = BeautifulSoup(response_traditional.content, 'html.parser')

    # Extract traditional season stats
    table_traditional = soup_traditional.find('table', {'class': 'nba-stat-table'})
    df_traditional = pd.read_html(str(table_traditional))[0]

    return df_traditional

def getAdvancedStats():

    return



def driver():
    teamsURL = r'https://www.basketball-reference.com/teams/'

    teamsFilePath = r'nbaTeams.txt'
    teamsDict = getTeamDict(teamsFilePath)

    teamsTraditionalURL = r'https://www.nba.com/stats/teams/traditional'
    teamsAdvancedURL = r'https://www.nba.com/stats/teams/advanced'

    print(getTraditionalStats(teamsTraditionalURL))

    
driver()