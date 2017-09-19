import pandas as pd
from glob import glob
import matplotlib.pyplot as plt

files = glob('wtc*elo.json')
df = pd.DataFrame()

results = [pd.read_json(f) for f in files]
df = pd.concat(results, ignore_index=True)

# now get a sorted list of unique players
players = df.player.unique()

years = [2013 + i for i in range(4)]

# make a figure
f, ax = plt.subplots(1)

i = 0
for y in years:
    for p in players:
        r = df[(df.player == p) & (df.year == y)]
        r = r.sort_values('round')
        #if r.faction.any() == 'Circle Orboros':
        #    ax.plot(r['round'] + i, r.elo_current, c='r', alpha=0.6, zorder=99)
        #else:
        ax.plot(r['round'] + i, r.elo_current, c='0.6', alpha=0.6)

    if not i:
        i += 5
    else:
        i += 6

    ax.axvline(i + 0.5, c='0.9')

