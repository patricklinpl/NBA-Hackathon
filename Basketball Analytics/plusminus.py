#!/usr/bin python3

import os
import pandas as pd

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
        Object: 

        {
            game_id: {
                team_1: score,
                team_2: score
            }
        }

    """

    league_matches = {}

    unique_pairs = pd.read_csv('results/NBA Hackathon - Game Lineup Data Sample (50 Games).csv', usecols=['Game_id', 'Team_id'])
    unique_pairs.drop_duplicates(subset=['Game_id', 'Team_id'], inplace=True)

    for i, row in unique_pairs.iterrows():
        game_id = row['Game_id']
        team_id = row['Team_id']
        if league_matches.get(game_id) is None:
            league_matches[game_id] = {}
        league_matches[game_id][team_id] = 0
    
    return league_matches

def calc_plus_minus():
    write_csv('data/', 'results/')
    league_matches = filter_league_matches()

calc_plus_minus()