import os
import pandas as pd

def csv_generator(inputPath, outputPath):
    """This function is used to convert input .txt to .csv

    Args:
        param1 (str): The path to provided sample data.
        param2 (str): The path to output folder.

    Yields:
        bool: Writes the csv to path. True for success. False otherwise.

    """
    for file in os.listdir(inputPath):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            df = pd.read_table(inputPath + filename)
            if ("Play" in filename):
                df = df.sort_values(by=['Game_id', 'Period', 'PC_Time', 'WC_Time', 'Event_Num'], ascending=[True, True, False, True, True])
            if ("Lineup" in filename): 
                plus_minus = pd.read_table(inputPath + filename, usecols=['Game_id', 'Person_id'])
                plus_minus['Player_Plus/Minus'] = ''
                plus_minus.to_csv('results/Q1_BBALL.csv', index=False) 
            df.to_csv(outputPath + filename.split(".")[0] + '.csv', index=False)

    return True

csv_generator('data/', 'results/')