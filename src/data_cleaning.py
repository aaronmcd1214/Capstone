import pandas as pd
import numpy as np

def initial_drop(df):
    """
    This function takes the pandas DataFrame containing offensive statistics and
    drops some rows that do not contribute a player's production

    Args:
        df: pandas DataFrame object
    Returns:
        nothing, df is acted on inplace
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
    print('Combining multiple stints into single years...')
    df = df.groupby(['playerID', 'yearID']).sum()
    return df.reset_index(level=['playerID', 'yearID'])

def map_position(batting_df, fielding_df):
    """
    This function will use a DataFrame of fielding statistics to find each players'
    most played position and then add that position to the batting_df

    Args:
        batting_df: pandas DataFrame object
        fielding_df: pandas DataFrame object
    Returns:
        nothing, batting_df is acted on inplace
    """
    print('Mapping positions to batting stats...')
    for player in fielding_df['playerID'].unique():
        idxmax = fielding_df[fielding_df['playerID'] == player]['POS'].value_counts().idxmax()
        batting_df.loc[batting_df['playerID'] == player, 'pos'] = idxmax
    batting_df_dropped_p = batting_df.drop(batting_df[batting_df['pos'] == 'P'].index) #drop pitchers
    batting_df_dropped_p_null = batting_df_dropped_p.dropna() #drop players with no position

    return batting_df_dropped_p_null

def create_averages(df):
    """
    This function creates a new DataFrame that contains each player's averages
    of each statistic over the course of their career

    Args:
        df: pandas DataFrame object
    Returns:
        New DataFrame object
    """
    print('Creating DataFrame of averages...')
    avg_df = df.drop('yearID', axis=1)
    avg_df = avg_df.groupby('playerID').mean()
    avg_df['total_seasons'] = [len(df[df['playerID'] == player]) for player in df['playerID'].unique()]
    return avg_df.round(3)
