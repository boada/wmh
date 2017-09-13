import pandas as pd
from elo import pwin, new_elo
import numpy as np

df2013 = pd.read_json('wtc_data/wtc2013_results.json')
df2013['pwin'] = pd.Series(np.ones(len(df2013)))
df2013['elo_current'] = pd.Series(1500 * np.ones(len(df2013)))
df2013['elo_new'] = pd.Series(1500 * np.ones(len(df2013)))

for i in np.sort(df2013.match.unique()):
    match = df2013.loc[df2013.match == i]
    player1 = df2013.loc[df2013.player == match.player.iloc[0]]
    player2 = df2013.loc[df2013.player == match.player.iloc[1]]


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

    df2013.loc[df2013.match == i, 'elo_current'] = [p1_elo_old, p2_elo_old]
    df2013.loc[df2013.match == i, 'pwin'] = [p1_pwin, p2_pwin]
    df2013.loc[df2013.match == i, 'elo_new'] = [p1_elo_new, p2_elo_new]


