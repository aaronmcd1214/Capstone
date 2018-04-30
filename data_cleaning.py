import pandas as import pd
import numpy as np

def initial_drop(df):
    """
    This function takes the pandas DataFrame containing offensive statistics and
    drops some rows that do not contribute a player's production

    Args:
        df: pandas DataFrame object
    """
    drop_list = ['teamID', 'lgID', 'stint']
    df.drop(drop_list, inplace=True, axis=1) #cols are dropped inplace, no return necessary

def combine_stints(df):
    """
    This function takes a pandas DataFrame and combines multiple 'stints' in one
    year into one total row for the year regardless of the team played for or league
    played in

    Args:
        df: pandas DataFrame object
    Returns:
        pandas DataFrame object that has combined players' stats across 'stints'
    """
    df = df.groupby(['playerID', 'yearID']).sum()
    return df.reset_index(level=['playerID', 'yearID'])

def create_averages(df):
    """
    This function creates a new DataFrame that contains each player's averages
    of each statistic over the course of their career

    Args:
        df: pandas DataFrame object
    Returns:
        New DataFrame object
    """
    avg_df = df.drop('yearID', axis=1)
    avg_df = avg_df.groupby('playerID').mean()
    avg_df['total_seasons'] = [len(df[df['playerID'] == player]) for player in df['playerID'].unique()]
    return avg_df
