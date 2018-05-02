from src import data_cleaning as dc
import pandas as pd
import sys

class PlayerPrediction(object):
    def __init__(self, player_name=None, playerID=None):
        self.player_name = player_name

        if playerID == None:
            self.playerID = get_id(player_name)
        else:
            self.playerID = playerID
        self.build_dataframes()
        # build_models()
        # predict()
        # display_results()

    def get_id(player_name):
        pass

    def build_dataframes(self):
        #initial DataFrames created
        print('Building DataFrames and engineering features/cleaning...')
        master_df = pd.read_csv('src/data/baseballdatabank-master/core/People.csv')
        batting_df = pd.read_csv('src/data/baseballdatabank-master/core/Batting.csv')
        fielding_df = pd.read_csv('src/data/baseballdatabank-master/core/Fielding.csv')

        if self.player_name == None:
            first = master_df.loc[master_df['playerID'] == self.playerID, 'nameFirst'].iloc[0]
            last = master_df.loc[master_df['playerID'] == self.playerID, 'nameLast'].iloc[0]
            self.player_name = first + ' ' + last
        #initial feature drop
        dc.initial_drop(batting_df)

        #combine stints to single years
        batting_df_stints_combined = dc.combine_stints(batting_df)

        #create avg_df, contains players' averages over career
        self.avg_df = dc.create_averages(batting_df_stints_combined)

        #map most-played position to the batting_df and drop pitchers and those without a position
        batting_pos_df = dc.map_position(batting_df_stints_combined, fielding_df)

        #pull out players of same position and at least as many years as self.playerID
        self.players_to_compare = self._get_comparison(batting_pos_df)

    def _get_comparison(self, df):
        """
        This function receives a DataFrame and returns a new DataFrame that contains
        the players who have as much experience as the player to be projected

        Args:
            df: pandas DataFrame object
        Returns:
            filtered DataFrame
        """
        #get player's position
        player_pos = df.loc[df['playerID'] == self.playerID, 'pos'].unique()[0]

        #set masks
        player_mask = df['playerID'] == self.playerID
        pos_mask = df['pos'] == player_pos

        #get years of service
        years_served = len(df[player_mask])

        #get players of same position
        same_pos = df.loc[(~player_mask) & (pos_mask)]

        #filter players of same position and their first n years equal to self.playerID's service time
        first_n_years = same_pos.groupby('playerID', as_index=False).head(years_served)

        #filter out players with service time less than self.playerID
        return self._players_to_compare_func(first_n_years)

    def _players_to_compare_func(self, df):
        """
        This function filters the passed in DataFrame to remove players who don't
        have at least the same amount of years of service as the player to be projected

        Args:
            df: pandas DataFrame object
        Returns:
            filtered DataFrame
        """
        value_counts = df.playerID.value_counts()
        players_to_compare = value_counts.loc[value_counts.values == 7].index
        return df[df['playerID'].isin(players_to_compare)]


    def build_models(self, playerID):
        pass

    def predict(self):
        pass

    def display_results(self):
        pass

if __name__ == '__main__':
    """
    Code will be built here so that the script can be run from the command line
    as such: python fetch_data.py <player name>.  This script will then use the
    provided player name to find similar players and predict future offensive
    production
    """
