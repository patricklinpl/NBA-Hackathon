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

def process_game_logs(league_matches, match_starters):
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
    free_throw = False
    free_throw_score = 0
    update_players = []

    for i, row in play_by_play.iterrows():
        game_id = row['Game_id']
        team_id = row['Team_id']
        event = row['Event_Msg_Type']
        action = row['Action_Type']
        option = row['Option1']
        player = row['Person1']
        sub = row['Person2']
        period = row['Period']

        game = league_matches[game_id]

        if game.get(team_id) is None:
            continue
        
        if (event is not 3) and (event is not 8):
            update_players = []

        if event is 1:
            league_matches[game_id][team_id]['box_score'] += option
        
        if (event is 3) and (option > 0) and (action is not 0):
            league_matches[game_id][team_id]['box_score'] += 1

            if (len(update_players) > 0):
                for player in update_players:
                    current_team = team_id
                    opponent = getOpponent(game, team_id)

                    if (match_starters[game_id][team_id][period].get(player)) is None:
                        current_team = opponent
                        opponent = team_id
                    
                    if team_id is current_team:
                        league_matches[game_id][current_team][player] += 1
                    else:
                        league_matches[game_id][current_team][player] -= 1 
        
        if (event is 8) or (event is 11):
            current_team = team_id
            opponent = getOpponent(game, team_id)

            if (match_starters[game_id][team_id][period].get(player)) is None:
                current_team = opponent
                opponent = team_id
            
            if (league_matches[game_id][current_team].get(sub)) is None:
                league_matches[game_id][current_team][sub] = 0

            league_matches[game_id][current_team][player] = (league_matches[game_id][current_team]['box_score'] - league_matches[game_id][opponent]['box_score'])
            match_starters[game_id][current_team][period][player] = False 
            match_starters[game_id][current_team][period][sub] = True
            update_players.append(player)

        if event is 13:
            teams = list(match_starters[game_id].keys())

            for unique_team in teams:
                opponent = getOpponent(game, unique_team) 
                players = list(match_starters[game_id][unique_team][period].keys())

                for unique_player in players:

                     if match_starters[game_id][unique_team][period][unique_player] is True:
                         league_matches[game_id][unique_team][unique_player] = league_matches[game_id][unique_team][unique_player] + (league_matches[game_id][unique_team]['box_score'] - league_matches[game_id][opponent]['box_score'])

    return (league_matches, match_starters)

def getOpponent(game, team_id):
    team_keys = [*game]
    opponent = list(filter(lambda x: x != team_id , team_keys))[0]
    return opponent

def calc_plus_minus():
    league_matches, match_starters = process_match_lineups()
    #print(league_matches['021fd159b55773fba8157e2090fe0fe2'])
    res1, res2 = process_game_logs(league_matches, match_starters)
    # print(res2['021fd159b55773fba8157e2090fe0fe2']['012059d397c0b7e5a30a5bb89c0b075e'])
    print(res1['021fd159b55773fba8157e2090fe0fe2']['012059d397c0b7e5a30a5bb89c0b075e'])
    print('')
    print('')
    print(res1['021fd159b55773fba8157e2090fe0fe2']['cff694c8186a4bd377de400e4f60fe47'])

calc_plus_minus()