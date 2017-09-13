import pandas as pd
from elo import pwin, new_elo
import numpy as np
from optparse import OptionParser

def init_tounament(df, initFrom):
    ''' This function initializes the elo scores using the ending score from
    the previous year's tournament. If the player didn't play in the previous
    year then they get the default value of 1500.

    @type df: pandas.DataFrame
    @param df: Current tournament dataframe
    @type initFrom: into
    @param initFrom: Previous year to use for the initialization
    @rtype: pandas.DatFrame
    @return: The initialized dataframe for the current tournament.

    '''

    old_df = pd.read_json('wtc{}_results_elo.json'.format(initFrom))

    # now get a sorted list of unique players
    players = old_df.player.unique()

    # get the last rounds elo rating
    rounds = old_df['round'].max()

    # get the mean elo from the previous tournament
    # we'll correct by this going into the new tournament
    elo_mean = old_df.elo_new.loc[(old_df['round'] == rounds)].mean()

    # move the ratings into the init spot of the new tournament
    for p in players:
        elo = old_df.elo_new.loc[(old_df.player == p) &
                                 (old_df['round'] == rounds)].values[0]

        # correct this elo rating for the new tournament
        # move toward the mean by 1/3 of the difference
        # this is taken from fivethirtyeight
        elo_c = elo - (elo - elo_mean) / 3

        df.loc[(df.player == p) & (df['round'] == 1), 'elo_current'] = elo_c

    return df

def score_tournament(df):
    ''' Does all of the elo scoring for the entire tournament. Handles all of
    the updating of the dataframe. The final elo standings for the players are
    defined as the 'elo_current' for the final round. It is this value that
    will be used to initialize a future year's tournament if that is desired.

    @type df: pandas.DataFrame
    @param df: The current tournament for which we are running the scoring.
    @rtype: pandas.DataFrame
    @return: The scored dataframe for the current tournament.

    '''

    for i in np.sort(df.match.unique()):
        match = df.loc[df.match == i]
        player1 = df.loc[df.player == match.player.iloc[0]]
        player2 = df.loc[df.player == match.player.iloc[1]]

        # get the previous round number
        round_number = match['round'].iloc[0]
        if round_number == 1:
            pround_number = 1
        else:
            pround_number = round_number - 1

        p1_pwin = pwin(player1.loc[player1['round'] == pround_number,
                                'elo_current'].values[0],
                                player2.loc[player2['round'] == pround_number,
                                'elo_current'].values[0])
        p2_pwin = pwin(player2.loc[player2['round'] == pround_number,
                                'elo_current'].values[0],
                                player1.loc[player1['round'] == pround_number,
                                'elo_current'].values[0])

        if round_number == 1:
            p1_elo_old = player1.loc[player1['round'] == pround_number,
                                     'elo_current'].values[0]

            p1_elo_new = new_elo(p1_elo_old, p1_pwin,
                                player1.loc[player1['round'] == round_number,
                                            'win'].values[0])

            p2_elo_old = player2.loc[player2['round'] == pround_number,
                                      'elo_current'].values[0]

            p2_elo_new = new_elo(p2_elo_old, p2_pwin,
                                player2.loc[player2['round'] == round_number,
                                            'win'].values[0])

        else:
            p1_elo_old = player1.loc[player1['round'] == pround_number,
                                     'elo_new'].values[0]

            p1_elo_new = new_elo(p1_elo_old, p1_pwin,
                                player1.loc[player1['round'] == round_number,
                                            'win'].values[0])

            p2_elo_old = player2.loc[player2['round'] == pround_number,
                                     'elo_new'].values[0]

            p2_elo_new = new_elo(p2_elo_old, p2_pwin,
                                player2.loc[player2['round'] == round_number,
                                            'win'].values[0])

        df.loc[df.match == i, 'elo_current'] = [p1_elo_old, p2_elo_old]
        df.loc[df.match == i, 'pwin'] = [p1_pwin, p2_pwin]
        df.loc[df.match == i, 'elo_new'] = [p1_elo_new, p2_elo_new]

    return df


if __name__ == "__main__":

    # Read in the command line options
    USAGE = '''usage:\t %prog <year> [options]
    i.e.: %prog 2013'''

    parser = OptionParser(usage=USAGE)

    parser.add_option("--init-from",
                      action="store",
                      dest="initFrom",
                      default=0,
                      help='Previous year from which to initialize the new '
                            'tournament')

    (opt, args) = parser.parse_args()

    # read the data from the desired year
    df = pd.read_json('wtc_data/wtc{}_results.json'.format(args[0]))

    # create the columns and fill with initial data
    df['pwin'] = pd.Series(np.ones(len(df)))
    df['elo_current'] = pd.Series(1500 * np.ones(len(df)))
    df['elo_new'] = pd.Series(1500 * np.ones(len(df)))

    if opt.initFrom:
        df = init_tounament(df, opt.initFrom)

    df = score_tournament(df)

