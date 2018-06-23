#!/usr/bin python3

import pandas as pd
import numpy as np

def process_match_lineups():
    """This function is used to make a dictionary to hold unique match ups to track box scores

    Returns:
        object: {
            game_id: {
                team_1: {
                    player_1: plus_minus,
                    player_2: plus_minus, 
                    etc..
                },
                team_2: {
                    player_1: plus_minus,
                    player_2: plus_minus, 
                    etc..
                },
            }
        }

    """

    league_matches = {}
    match_starters = {}

    match_lineups = pd.read_csv('results/NBA Hackathon - Game Lineup Data Sample (50 Games).csv')

    for i, row in match_lineups.iterrows():
        game_id = row['Game_id']
        team_id = row['Team_id']
        person_id = row['Person_id']
        period = row['Period']

        if league_matches.get(game_id) is None:
            league_matches[game_id] = {}
            match_starters[game_id] = {}
        
        if league_matches[game_id].get(team_id) is None:
            league_matches[game_id][team_id] = {}
            match_starters[game_id][team_id] = {}

        if league_matches[game_id][team_id].get('box_score') is None:
            league_matches[game_id][team_id]['box_score'] = 0
        
        league_matches[game_id][team_id][person_id] = 0
        
        if match_starters[game_id][team_id].get(period) is None:
            match_starters[game_id][team_id][period] = {}
        
        match_starters[game_id][team_id][period][person_id] = True
    
    return (league_matches, match_starters)

def process_game_logs(league_matches):
    """This function is used to determine the action to take from each play by plays

    Args:
        league_matches (object): the dictionary containing initial data

   Returns:
        object: {
            game_id: {
                team_1: {
                    box_score: score,
                    player_1: plus_minus,
                    player_2: plus_minus, 
                    etc..
                },
                team_2: {
                    box_score: score,
                    player_1: plus_minus,
                    player_2: plus_minus, 
                    etc..
                },
            }
        }

    """

    play_by_play = pd.read_csv('results/NBA Hackathon - Play by Play Data Sample (50 Games).csv', dtype={'Event_Msg_Type': np.int8, 'Period': np.int8, 'Action_Type': np.int8, 'Option1': np.int8})

    for i, row in play_by_play.iterrows():
        game_id = row['Game_id']
        team_id = row['Team_id']
        event = row['Event_Msg_Type']
        action = row['Action_Type']
        option = row['Option1']
        player = row['Person1']

        game = league_matches[game_id]

        # if row['Period'] is 2:
        #     break

        if game.get(team_id) is None:
            continue

        if event is 1:
            league_matches[game_id][team_id]['box_score'] += option
        
        if (event is 3) and (option > 0) and (action is not 0):
            league_matches[game_id][team_id]['box_score'] += 1
        
        if (event is 8) or (event is 11) or (event is 13):
            team_keys = [*game]
            opponent = list(filter(lambda x: x != team_id , team_keys))[0]
            league_matches[game_id][team_id][player] = league_matches[game_id][team_id]['box_score'] - league_matches[game_id][opponent]['box_score'] 

    return league_matches


def calc_plus_minus():
    league_matches, match_starters = process_match_lineups()
    # print(match_starters['021fd159b55773fba8157e2090fe0fe2'])
    # res = process_game_logs(league_matches)
    # print(res['021fd159b55773fba8157e2090fe0fe2'])

calc_plus_minus()