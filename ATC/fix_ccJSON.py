import pandas as pd
import sys

def fix(lists):

    df = pd.read_json(lists)

    df2 = pd.DataFrame([p for p1 in df.players for p in p1])
    df2['theme1'] = ''
    df2['theme2'] = ''
    for i, l in df2.list2.iteritems():
        try:
            df2.theme2.iloc[i] = l['theme']
        except KeyError:
            continue
        except TypeError:
            continue
    for i, l in df2.list2.iteritems():
        try:
            df2.theme2.iloc[i] = l['theme']
        except KeyError:
            df2.theme2.iloc[i] = 'None'
        except TypeError:
            continue
    for i, l in df2.list1.iteritems():
        try:
            df2.theme1.iloc[i] = l['theme']
        except KeyError:
            df2.theme1.iloc[i] = 'None'
        except TypeError:
            continue
    for i, l in df2.list2.iteritems():
        try:
            df2.list2.iloc[i] = l['list']
        except KeyError:
            continue
        except TypeError:
            continue
    for i, l in df2.list1.iteritems():
        try:
            df2.list1.iloc[i] = l['list']
        except KeyError:
            continue
        except TypeError:
            continue

    df2.to_json('fixed.json')


if __name__ == "__main__":
        fix(sys.argv[1])
