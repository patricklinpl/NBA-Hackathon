#!/usr/bin python3

import pandas as pd
import numpy as np

def process_match_lineups():
    """This function is used to make two dictionaries to a) hold unique match ups to track box scores 
       b) track players on the floor after each period

    Returns:
        league_matches: {
            game_id: {
                team_1: {
                    box_score: 0,
                    player_1: plus_minus,
                    player_2: plus_minus, 
                    etc..
                },
                team_2: {
                    box_score: 0,
                    player_1: plus_minus,
                    player_2: plus_minus, 
                    etc..
                },
            }
        }
        
        match_starters: {
            game_id: {
                period_1: {
                    team_1: {
                        player_1: true,
                        player_2: true,
                        etc..
                    },
                    team_2: {
                        player_1: true,
                        player_2: true,
                        etc..
                    },
                },
                period_2: {
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
    """This function is used to determine the action to take from the play by log

    Args:
        league_matches (object): the dictionary containing box score & player plus minus 
        match_starters (object): the dictionary containing the starters & active players for every period

   Returns:
        object: league_matches - see process_match_lineups() for data structure

    """

    play_by_play = pd.read_csv('results/NBA Hackathon - Play by Play Data Sample (50 Games).csv', 
                              dtype={'Event_Msg_Type': np.int8, 'Period': np.int8, 'Action_Type': np.int8, 'Option1': np.int8})
                              
    update_players_after_ft = []

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

        # continue for invalid team_id. e.g. game start
        if game.get(team_id) is None:
            continue
        
        # reset players to update if free throws are finished
        if (event is not 3) and (event is not 8):
            update_players_after_ft = []

        # update score when shot is made
        if event is 1:
            league_matches[game_id][team_id]['box_score'] += option
        
        # update score after a free throw 
        if (event is 3) and (option > 0) and (action is not 0):
            league_matches[game_id][team_id]['box_score'] += 1

            # update players subbed out during a free throw 
            if (len(update_players_after_ft) > 0):
                for player in update_players_after_ft:
                    current_team = team_id
                    opponent = getOpponent(game, team_id)

                    if (match_starters[game_id][team_id][period].get(player)) is None:
                        current_team = opponent
                        opponent = team_id
                    
                    if team_id is current_team:
                        league_matches[game_id][current_team][player] += 1
                    else:
                        league_matches[game_id][current_team][player] -= 1 
        
        # calculate plus minus for players subbed out 
        if (event is 8) or (event is 11):
            current_team = team_id
            opponent = getOpponent(game, team_id)

            if (match_starters[game_id][team_id][period].get(player)) is None:
                current_team = opponent
                opponent = team_id
            
            if (league_matches[game_id][current_team].get(sub)) is None:
                league_matches[game_id][current_team][sub] = 0

            league_matches[game_id][current_team][player] += (league_matches[game_id][current_team]['box_score'] - league_matches[game_id][opponent]['box_score'])
            match_starters[game_id][current_team][period][player] = False 
            match_starters[game_id][current_team][period][sub] = True
            update_players_after_ft.append(player)

        # calculate plus minus for player at the end of the quarter 
        if event is 13:
            teams = list(match_starters[game_id].keys())

            for unique_team in teams:
                opponent = getOpponent(game, unique_team) 
                players = list(match_starters[game_id][unique_team][period].keys())

                for unique_player in players:
                     if match_starters[game_id][unique_team][period][unique_player] is True:
                         league_matches[game_id][unique_team][unique_player] += (league_matches[game_id][unique_team]['box_score'] - league_matches[game_id][opponent]['box_score'])

    return league_matches

def getOpponent(game, team_id):
    """This function determines the team_id of the opposing team 

    Args:
        game (object): A game dictionary containing the keys of both teams
        team_id (str): The current team id.

    Returns:
        str: The team_id of the opposing team

    """
    team_keys = [*game]
    opponent = list(filter(lambda x: x != team_id , team_keys))[0]
    return opponent

def write_plus_minus_csv(plus_minus_data):
    """This function writes the plus minus data 

    Args:
        plus_minus_data (object): A game dictionary containing the keys of both teams

    Returns:
        bool: True for success. False otherwise.

    """

    df = pd.read_csv('results/Q1_BBALL.csv')

    for i, row in df.iterrows():
        plus_minus = row['Player_Plus/Minus']
        game_id = row['Game_id']
        player = row['Person_id']

        current_game = plus_minus_data[game_id]
        team_keys = [*current_game]

        for team in team_keys:
            if plus_minus_data[game_id][team].get(player) is None:
                continue
            else:
                df.at[i, 'Person_id'] = plus_minus_data[game_id][team][player]
    
    df.to_csv('results/Q1_BBALL.csv', index=False)
    return True

def calc_plus_minus():
    """This function calculates the plus minus and writes a csv file 

    """
    league_matches, match_starters = process_match_lineups()
    results = process_game_logs(league_matches, match_starters)
    write_plus_minus_csv(results)

calc_plus_minus()