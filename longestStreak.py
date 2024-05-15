import statsapi
import time

# # https://statsapi.mlb.com/api/v1.1/game/179480/feed/live

# a = statsapi.get('game', {'gamePk':179480})
# b = a['gameData']['game']['gameNumber']
# print()


def GetTeamSeriesHistory(id,year):
    teamSeriesHistory = []
    start_date = '01/01/' + str(year)
    end_date = '01/01/' + str(year + 1)
    teamGameHistory = statsapi.schedule(start_date=start_date,end_date=end_date,team=id)
    currentTeam = teamIdDict[id]
    gameInSeries = 0
    for gameIndex in range(len(teamGameHistory)):
        game = teamGameHistory[gameIndex]
        if gameIndex == len(teamGameHistory) - 1:
            nextGame = {'home_name':None, 'away_name':None}
        else:
            nextGame = teamGameHistory[gameIndex + 1]
        if game['game_type'] not in ['S','A','I','E'] and game['status'] == 'Final':
            gameInSeries += 1
            if game['home_name'] != currentTeam:
                opponent = game['home_name']
            else:
                opponent = game['away_name']
            currentMatchUp = (game['home_name'], game['away_name'])
            nextMatchUp = (nextGame['home_name'], nextGame['away_name'])

            if opponent not in nextMatchUp:
                if teamAbbreviationDict[id] in game['series_status'] and 'wins' in game['series_status']:
                    teamSeriesHistory.append((opponent, gameInSeries, 'W'))
                elif teamAbbreviationDict[id] not in game['series_status'] and 'wins' in game['series_status']:
                    teamSeriesHistory.append((opponent, gameInSeries, 'L'))
                elif 'tied' in game['series_status']:
                    teamSeriesHistory.append((opponent, gameInSeries, 'D'))
                else:
                    print("BIG ERROR WTF")
                gameInSeries = 0

    return teamSeriesHistory

            # if game['game_type'] != 'R':
            #     if opponent not in nextMatchUp:
            #         if teamAbbreviationDict[id] in game['series_status'] and 'wins' in game['series_status']:
            #             teamSeriesHistory.append((opponent, gameInSeries, 'W'))
            #         elif teamAbbreviationDict[id] not in game['series_status'] and 'wins' in game['series_status']:
            #             teamSeriesHistory.append((opponent, gameInSeries, 'L'))
            #         elif 'tied' in game['series_status']:
            #             teamSeriesHistory.append((opponent, gameInSeries, 'D'))
            #         gameInSeries = 0


            # if game['game_type'] == 'R':
            #     if nextMatchUp != currentMatchUp:
            #         if teamAbbreviationDict[id] in game['series_status'] and 'wins' in game['series_status']:
            #             teamSeriesHistory.append((opponent, gameInSeries, 'W'))
            #         elif teamAbbreviationDict[id] not in game['series_status'] and 'wins' in game['series_status']:
            #             teamSeriesHistory.append((opponent, gameInSeries, 'L'))
            #         elif 'tied' in game['series_status']:
            #             teamSeriesHistory.append((opponent, gameInSeries, 'D'))
            #         else:
            #             print("BIG ERROR WTF")
            #         gameInSeries = 0
                    
    # return teamSeriesHistory



# teamIds = []
# teamIdDict = {}
# teamAbbreviationDict = {}
# allTeams = statsapi.get('teams', {})
# for team in allTeams['teams']:
#     if team['sport']['id'] == 1:
#         teamIds.append(team['id'])
#         teamIdDict[team['id']] = team['name']
#         teamAbbreviationDict[team['id']] = team['abbreviation']



teamAbbreviationDict = {}
teamAbbreviationDict[142] = 'MIN'
teamIds = [142]
teamIdDict = {}
teamIdDict[142] = 'Minnesota Twins'

allTeamsSeriesHistory = {}

for id in teamIds:
    allTeamsSeriesHistory[teamIdDict[id]] = []

for id in teamIds:
    for year in range(1980, 1990):
        allTeamsSeriesHistory[teamIdDict[id]] += GetTeamSeriesHistory(id,year)
        time.sleep(30)
        print()


f = open("Twins1980-1990SeriesRecord.txt", "w")
for team, history in allTeamsSeriesHistory.items():
    f.write('%s:%s\n' % (team, history))
f.close()




# sport_ids = statsapi.get('sports', {})
# for x in sport_ids['sports']:
#     print(x['name'])