import pandas as pd
from glob import glob
from string import capwords
import numpy as np

def levenshtein(source, target):
    if len(source) < len(target):
        return levenshtein(target, source)

    # So now we have len(source) >= len(target).
    if len(target) == 0:
        return len(source)

    # We call tuple() to force strings to be used as sequences
    # ('c', 'a', 't', 's') - numpy uses them as values by default.
    source = np.array(tuple(source))
    target = np.array(tuple(target))

    # We use a dynamic programming algorithm, but with the
    # added optimization that we only need the last two rows
    # of the matrix.
    previous_row = np.arange(target.size + 1)
    for s in source:
        # Insertion (target grows longer than source):
        current_row = previous_row + 1

        # Substitution or matching:
        # Target and source items are aligned, and either
        # are different (cost of 1), or are the same (cost of 0).
        current_row[1:] = np.minimum(
                current_row[1:],
                np.add(previous_row[:-1], target != s))

        # Deletion (target grows shorter than source):
        current_row[1:] = np.minimum(
                current_row[1:],
                current_row[0:-1] + 1)

        previous_row = current_row

    return previous_row[-1]


files = glob('wtc_data/wtc*_results.json')

#make a new dataframe
df = pd.DataFrame()

results = [pd.read_json(f) for f in files]

# make sure first and last names are capitalized. also removes leading and
# trailing white space.
for r in results:
    for i, p in r.player.iteritems():
        r.loc[i, 'player'] = capwords(p)

df = pd.concat(results, ignore_index=True)

# now get a sorted list of unique players
players = df.player.unique()
players = np.sort(players)

# some of the player names will be very close. AKA misspellings. We can get a
# list of those using the levenshtein function.

name_fix = {}

for i, p in enumerate(players):
    for j in range(4):
        try:
            dist = levenshtein(players[i], players[i + j + 1])
        except IndexError: # we are running off the end
            continue
        if dist <= 2:
            print(players[i], players[i + j + 1])
            name_fix[players[i]] = players[i + j + 1]

# this should be visually inspected to make sure it looks good before replacing
# names in the data files. I manually removed 1 item and tweaked a second to
# make sure things worked out.
# After the visual inspect you can run the following code to update all of the
# data frames.

# manual edits:
# del name_fix['David Kane']
# del name_fix['Maurus Markwalder']
# name_fix['Maurus Markwalder:'] = 'Maurus Markwalder'

if False:
    for r in results:
        for n in name_fix:
            r.loc[r['player'] == 'Maurus Markwalder:', 'player'] = 'Maurus Markwalder'

# After this point. You can update the number of changes in the levenshtein
# function to 3 (line 74) and rerun things. This gives a few more changes, most
# of which aren't real changes. I did update a few at this point 'Matt' ->
# 'Matthew' for example. Again, this has to be done interactive, to avoid names
# that really shouldn't be changed.

# Here are the changes:

# name_fix['Jay Mcleod'] = 'Jason Mcleod'
# name_fix['Freek Punt'] = 'Frederik Punt'
# name_fix['Nikos Kerazoglou'] = 'Nikolaos Kerazoglou'
# name_fix['Michal Konieczny'] = 'Michal Nakonieczny' -- this is incorrect
# name_fix['Matt Goligher'] =  'Matthew Goligher'
