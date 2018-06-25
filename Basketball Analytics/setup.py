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

write_csv('data/', 'results/')