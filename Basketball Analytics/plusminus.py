#!/usr/bin python3

import os
import pandas as pd
import numpy as np

def write_csv(inputPath, outputPath):
    """This function is used to convert input .txt to .csv

    Args:
        inputPath (str): The path to provided sample data.
        outputPath (str): The path to output folder.

    Returns:
        bool: Writes the csv to path. True for success. False otherwise.

    """
    for file in os.listdir(inputPath):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            df = pd.read_table(inputPath + filename)
            if ("Play" in filename):
                df.sort_values(by=['Game_id', 'Period', 'PC_Time', 'WC_Time', 'Event_Num'], ascending=[True, True, False, True, True], inplace=True)
            if ("Lineup" in filename): 
                plus_minus = pd.read_table(inputPath + filename, usecols=['Game_id', 'Person_id'])
                plus_minus['Player_Plus/Minus'] = ''
                plus_minus.to_csv('results/Q1_BBALL.csv', index=False) 
            df.to_csv(outputPath + filename.split(".")[0] + '.csv', index=False)

    return True

def filter_league_matches():
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

    unique_pairs = pd.read_csv('results/NBA Hackathon - Game Lineup Data Sample (50 Games).csv', usecols=['Game_id', 'Person_id', 'Team_id'])
    unique_pairs.drop_duplicates(subset=['Game_id', 'Person_id', 'Team_id'], inplace=True)

    for i, row in unique_pairs.iterrows():
        game_id = row['Game_id']
        team_id = row['Team_id']
        person_id = row['Person_id']

        if league_matches.get(game_id) is None:
            league_matches[game_id] = {}
        
        game = league_matches[game_id]
        
        if game.get(team_id) is None:
            game[team_id] = {}

        team = league_matches[game_id][team_id]

        if team.get('box_score') is None:
            team['box_score'] = 0

        team[person_id] = 0
    
    return league_matches

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

    play_by_play = pd.read_csv('results/NBA Hackathon - Play by Play Data Sample (50 Games).csv', dtype={'Event_Msg_Type': np.int8, 'Period': np.int8, 'Action_Type': np.int8, 'Option1': np.int8, 'Option2': np.int8, 'Option3': np.int8})

    for i, row in play_by_play.iterrows():
        game_id = row['Game_id']
        team_id = row['Team_id']
        event = row['Event_Msg_Type']
        action = row['Action_Type']
        option = row['Option1']
        player = row['Person1']

        game = league_matches[game_id]

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
    write_csv('data/', 'results/')
    league_matches = filter_league_matches()
    res = process_game_logs(league_matches)

calc_plus_minus()