import pandas as pd
from collections import OrderedDict

data = pd.read_csv('data/atp_matches_2021.csv', header=[0])

def get_records():
    record = {}

    for i in range(0, data.shape[0]):
        winner_name = data.at[i, 'winner_name']
        loser_name = data.at[i, 'loser_name']
        try:
            record[winner_name]['wins'] += 1
            try:
                record[winner_name]['%'] = float(record[winner_name]['wins']/record[winner_name]['losses']) * 100
            except ZeroDivisionError: 
                record[winner_name]['%'] = 100.0
        except KeyError:
            record[winner_name] = {'wins': 1, 'losses': 0, '%': 100.0}
        try:
            record[loser_name]['losses'] += 1
            record[loser_name]['%'] = float(record[loser_name]['wins']/record[loser_name]['losses']) * 100
        except KeyError:
            record[loser_name] = {'wins': 0, 'losses': 1, '%': 0.0}

    # for elem in record.items():
    #     print(elem)
    for elem in sorted(record.items(), key=lambda item: float(item[1]['%']),
            reverse=True):
        print(elem)


def main():
    print(data)

if __name__ == "__main__":
    main()
