from src import data_cleaning as dc
import pandas as pd
import sys


class PlayerPrediction(object):
    def __init__(self, player_id):
        self.master_df = pd.read_csv('src/data/baseballdatabank-master/core/People.csv')
        self.batting_df = pd.read_csv('src/data/baseballdatabank-master/core/Batting.csv')
        self.fielding_df = pd.read_csv('src/data/baseballdatabank-master/core/Fielding.csv')
        self.player_id = player_id
        first = self.master_df.loc[self.master_df['playerID'] == self.player_id, 'nameFirst'].iloc[0]
        last = self.master_df.loc[self.master_df['playerID'] == self.player_id, 'nameLast'].iloc[0]
        self.full_name = first + ' ' + last
        self.build_dataframes()
        # build_models()
        # predict()
        # display_results()

    """
    implement this method if time allows, otherwise just use player's id

    def get_id(self, player_name):
        self.master_df['nameFull'] = self.master_df['nameFirst'] + ' ' + self.master_df['nameLast']
    """

    # def get_full_name(self):
    #     first = self.master_df.loc[self.master_df['playerID'] == self.player_id, 'nameFirst'].iloc[0]
    #     last = self.master_df[self.master_df['playerID'] == self.player_id, 'nameLast'].iloc[0]
    #     return first + ' ' + last

    def build_dataframes(self):
        # initial DataFrames created
        print('Building DataFrames and engineering features/cleaning...')

        # initial feature drop
        dc.initial_drop(self.batting_df)

        # combine stints to single years
        batting_df_stints_combined = dc.combine_stints(self.batting_df)

        # # create avg_df, contains players' averages over career
        # self.avg_df = dc.create_averages(batting_df_stints_combined)

        # map most-played position to the batting_df and drop pitchers and those without a position
        self.batting_pos_df = dc.map_position(batting_df_stints_combined, self.fielding_df)

        # pull out players of same position and at least as many years as self.playerID
        self.players_to_compare = self._get_comparison(self.batting_pos_df)

    def _get_comparison(self, df):
        """
        This function receives a DataFrame and returns a new DataFrame that contains
        the players who have as much experience as the player to be projected

        Args:
            df: pandas DataFrame object
        Returns:
            filtered DataFrame
        """
        # get player's position
        player_pos = df.loc[df['playerID'] == self.player_id, 'pos'].unique()[0]

        # set masks
        player_mask = df['playerID'] == self.player_id
        pos_mask = df['pos'] == player_pos

        # get years of service
        self.years_served = len(df[player_mask])

        # get players of same position
        same_pos = df.loc[pos_mask]

        # filter players of same position and their first n years equal to self.playerID's service time
        first_n_years = same_pos.groupby('playerID', as_index=False).head(self.years_served)

        # filter out players with service time less than self.playerID
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
        players_to_compare = value_counts.loc[value_counts.values == self.years_served].index
        return df[df['playerID'].isin(players_to_compare)].reset_index()

    def build_models(self):
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
