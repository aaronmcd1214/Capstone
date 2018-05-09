import pandas as pd
import numpy as np
from collections import defaultdict

def initial_drop(df):
    """
    This function takes the pandas DataFrame containing offensive statistics and
    drops some rows that do not contribute a player's production

    Args:
        df: pandas DataFrame object
    Returns:
        pandas DataFrame
    """
    drop_list = ['teamID', 'lgID', 'stint']
    return df.drop(drop_list, axis=1) #cols are dropped inplace, no return necessary

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
        pandas DataFrame
    """
    print('Mapping positions to batting stats...')
    for player in fielding_df['playerID'].unique():
        idxmax = fielding_df[fielding_df['playerID'] == player]['POS'].value_counts().idxmax()
        batting_df.loc[batting_df['playerID'] == player, 'pos'] = idxmax
    batting_df_dropped_p = batting_df.drop(batting_df[batting_df['pos'] == 'P'].index)  # drop pitchers
    batting_df_dropped_p_null = batting_df_dropped_p.dropna()  # drop players with no position

    return batting_df_dropped_p_null

def condense_df(df0):
    """
    This function condenses all the rows of a players stats over time into one
    row of stats over time

    Args:
        df0: pandas DataFrame
    Returns:
        pandas DataFrame
    """
    df = df0.set_index('playerID')
    player_list = []
    for player in df.index.unique():
        def_dict = defaultdict(str)
        def_dict['playerID'] = player

        if isinstance(df.loc[player, 'pos'], str):
            def_dict['pos'] = df.loc[player, 'pos']
        else:
            def_dict['pos'] = df.loc[player, 'pos'].unique()[0]

        for col in df.columns:
            if col == 'yearID' or col == 'pos':
                continue
            try:
                for i, v in enumerate(df.loc[player, col]):
                    if i > 6:
                        continue
                    key = 'year' + str(i + 1) + '_' + col
                    def_dict[key] = v
            except:
                continue # skip players with only 1 year of data
        player_list.append(def_dict)
    new_df = pd.DataFrame(player_list)
    new_df_na_dropped = new_df.dropna() #drop players without 7 years of data
    new_df_w_dummies = pd.get_dummies(new_df_na_dropped, columns=['pos'])
    return new_df_w_dummies

def trim_batters(df):
    # remove those seasons where batter had less than 100 ABs
    df = df[df['AB'] > 100]

    # remove batters with less than 7 years experience
    s = df['playerID'].value_counts()
    df = df[df['playerID'].isin(s[s > 6].index)]

    # select first 7 seasons
    df = df.groupby('playerID').head(7)

    return df

# probably not needed
# def create_averages(df):
#     """
#     This function creates a new DataFrame that contains each player's averages
#     of each statistic over the course of their career
#
#     Args:
#         df: pandas DataFrame object
#     Returns:
#         New DataFrame object
#     """
#     print('Creating DataFrame of averages...')
#     avg_df = df.drop('yearID', axis=1)
#     avg_df = avg_df.groupby('playerID').mean()
#     avg_df['total_seasons'] = [len(df[df['playerID'] == player]) for player in df['playerID'].unique()]
#     return avg_df.round(3)
