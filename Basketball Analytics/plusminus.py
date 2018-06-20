import pandas as pd

def writeCSV():
    events = pd.read_table('data/NBA Hackathon - Event Codes.txt')
    lineup = pd.read_table('data/NBA Hackathon - Game Lineup Data Sample (50 Games).txt')
    plays = pd.read_table('data/NBA Hackathon - Play by Play Data Sample (50 Games).txt')

    events.to_csv('results/event_code.csv', index=False)
    lineup.to_csv('results/game_lineup.csv', index=False)
    plays.to_csv('results/play_by_play.csv', index=False)

    pd.read_table('data/NBA Hackathon - Game Lineup Data Sample (50 Games).txt', usecols=['Game_id', 'Person_id']).to_csv('results/Q1_BBALL.csv', index=False)
    plus_minus = pd.read_csv('results/Q1_BBALL.csv')
    plus_minus['Player_Plus/Minus'] = ''
    plus_minus.to_csv('results/Q1_BBALL.csv', index=False)   

    parsePlays()

def parsePlays():
    plays =  pd.read_csv('results/play_by_play.csv')
    sorted = plays.sort_values(by=['Game_id', 'Period', 'PC_Time', 'WC_Time', 'Event_Num'], ascending=[True, True, False, True, True])
    sorted.to_csv('results/sorted_plays.csv', index=False)
    print(sorted)

writeCSV()