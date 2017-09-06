import json
import pandas as pd
import sys

def fix(jsonFile):
    with open(jsonFile) as data_file:
        data = json.load(data_file)

    for grp in data['groups']:
        try:
            df2 = df2.append(grp['entries'], ignore_index=True)
        except NameError:
            df2 = pd.DataFrame(grp['entries'])
        except IndexError:
            pass

    df2.to_json(jsonFile)


if __name__ == "__main__":
    fix(sys.argv[1])

