import pandas as pd
import re 
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pprint import pprint
from collections import OrderedDict 
from requests_html import HTMLSession

#First Number is done status
#Name is for identifying links via espn
#Second Number is for iding whos playing who
#First List is the input aka stats coming into game 
#Second list is final score.
teams = {
    'ARI': [0, "arizona-cardinals", 1, [], []],
    'ATL': [0,"atlanta-falcons", 2, [], []],
    'BAL': [0, "baltimore-ravens", 3, [], []],
    'BUF': [0, "buffalo-bills", 4, [], []],
    'CAR': [0, "carolina-panthers", 5, [], []],
    'CHI': [0, "chicago-bears", 6, [], []],
    'CIN': [0, "cincinatti-bengals", 7, [], []],
    'CLE': [0, "cleveland-browns", 8, [], []],
    'DAL': [0, "dallas-cowboys", 9, [], []],
    'DEN': [0, "denver-broncos", 10, [], []],
    'DET': [0, "detroit-lions", 11, [], []],
    'GB': [0, "green-bay-packers", 12, [], []],
    'HOU': [0, "houston-texans", 13, [], []],
    'IND': [0, "indianapolis-colts", 14, [], []],
    'JAX': [0, "jacksonville-jaguars", 15, [], []],
    'KC': [0, "kansas-city-chiefs", 16, [], []],
    'LAC': [0, "los-angeles-chargers", 17, [], []],
    'LAR': [0, "los-angeles-rams", 18, [], []],
    'MIA': [0, "miami-dolphins", 19, [], []],
    'MIN': [0, "minnesota-vikings", 20, [], []],
    'NE': [0, "new-england-patriots", 21, [], []],
    'NO': [0, "new-orleans-saints", 22, [], []],
    'NYG': [0, "new-york-giants", 23, [], []],
    'NYJ': [0, "new-york-jets", 24, [], []],
    'OAK': [0, "oakland-raiders", 25, [], []],
    'PHI': [0, "philadelphia-eagles", 26, [], []],
    'PIT': [0, "pittsburgh-steelers", 27, [], []],
    'SF': [0, "san-francisco-49ers", 28, [], []],
    'SEA': [0, "seattle-seahawks", 29, [], []],
    'TB': [0, "tampa-bay-buccaneers", 30, [], []],
    'TEN': [0, "tennessee-titans", 31, [], []],
    'WSH': [0, "washington-redskins", 32, [], []]
}

url = "https://www.espn.com/nfl/schedule"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

data = [t.split(' ').pop() for t in [element.text for element in soup.find_all('a', attrs={'class': 'team-name'})]]
data = [tuple(data[i:i+2]) for i in range(0, len(data), 2)]
#Tuple, first element is away team, second element in home team.

team_data = []
for tup in data:
    #print(tup)
    for t in tup:
        print(t)
        if teams[t][0] == 1:
            #Team has bye week, is not currently playing, or has already been checked
            pass
        else:
            url = "https://www.espn.com/nfl/team/schedule/_/name/" + t.lower()
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')

            #Go through weeks and get game info for each team (regular season only)
            getids = re.findall("http://www.espn.com/nfl/game/_/gameId/.........", page.text)
            games = list(OrderedDict.fromkeys(getids))[:16]

            for game in games:
                url = game
                page = requests.get(url)
                soup = BeautifulSoup(page.text, 'html.parser')

                #Final score of game and currrent record after game
                #Use [0] instead of [1] to get just record
                records = [x.text.split(',')[1] for x in soup.find_all('div', attrs={'class': 'record'})]
                score = [x.text for x in soup.find_all('div', attrs={'class': 'score-container'})]
                #print(records, "\n")
                #print(score, "\n")

            #Currently experimenting with how to get team name without this since it is very long and inefficient
            """
            #Search for teams they have played against over the weeks
            for week in range(2,18):
                #Search for teams that they played against
                state = 0
                for te in teams.keys():
                    temp_str = str(week)
                    ser1 = soup.find('tr', attrs={'data-idx': temp_str})
                    search1 = ser1.find_all('a', attrs={'class': 'AnchorLink', 'href': '/nfl/team/_/name/' + te.lower() + '/' + teams[te][1]})
                    #Team has game this week
                    if len(search1) != 0:
                        teams[t][3].append([teams[te][2]])
                        state = 1
                        break 
                #Team has bye week on this week
                if state == 0:
                    teams[t][3].append([0])
            """
            teams[t][0] = 1 
         
pprint(teams)