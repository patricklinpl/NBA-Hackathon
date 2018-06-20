import pandas as pd

def clean():
    events = pd.read_table('../data/NBA Hackathon - Event Codes.txt')
    lineup = pd.read_table('../data/NBA Hackathon - Game Lineup Data Sample (50 Games).txt')
    plays = pd.read_table('../data/NBA Hackathon - Play by Play Data Sample (50 Games).txt')

    pd.read_table('../data/NBA Hackathon - Game Lineup Data Sample (50 Games).txt', usecols=['Game_id', 'Person_id']).to_csv('../results/Q1_BBALL.csv', index=False)

    result = pd.read_csv('../results/Q1_BBALL.csv')
    result['Player_Plus/Minus'] = ''
    result.to_csv('../results/Q1_BBALL.csv', index=False)

    print(result)
   

clean()