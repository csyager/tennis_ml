from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys
import re
import json
import csv
import random

try:
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
except Exception as e:
    print("Could not parse filename from command line arguments")
    exit(-1)

matches = pd.read_csv(input_filename, header=[0])

def compile_statistics():
    player_statistics = {}
    for i in range(0, matches.shape[0]):
        winner_name = matches.at[i, 'winner_name']
        loser_name = matches.at[i, 'loser_name']
        if winner_name not in player_statistics:
            player_statistics[winner_name] = {}
        if loser_name not in player_statistics:
            player_statistics[loser_name] = {}

    num_processed = 0
    num_players = len(player_statistics.keys())

    # beautiful soup configuration
    url = "https://www.minorleaguesplits.com/tennisabstract/cgi-bin/frags/"

    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'Referer': 'http://www.tennisabstract.com/cgi-bin/player.cgi?p=NovakDjokovic',
        'sec-ch-ua-mobile': '?0',
        'authority': 'www.minorleaguesplits.com',
        'if-modified-since': 'Sat, 11 Sep 2021 13:53:08 GMT',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'script',
        'referer': 'http://www.tennisabstract.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    not_found = []

    for player_name in player_statistics.keys():
        try:
            print(f"Parsing stats for player {player_name}")
            request_url = url + player_name.replace(" ", "") + ".js"
            response = requests.get(request_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find("table", id="pbp-stats")
            career_stats = table("tr")[-1]("td")

            # matches played
            try:
                matches_played = int(re.search("\((.*?)\)", career_stats[0].string).group(1).split()[0])
                player_statistics[player_name]['matches_played'] = matches_played
            except ValueError:
                player_statistics[player_name]['matches_played'] = 0

            # balanced leverage ratio
            try:
                blr = float(career_stats[2].string)
                player_statistics[player_name]['balanced_leverage_ratio'] = blr
            except ValueError:
                player_statistics[player_name]['balanced_leverage_ratio'] = 0.0

            # dominance ratio plus
            try:
                dr_plus = float(career_stats[3].string)
                player_statistics[player_name]['dominance_ratio_plus'] = dr_plus
            except ValueError:
                player_statistics[player_name]['dominance_ratio_plus'] = 0.0

            # excitement index
            try:
                excitement_index = float(career_stats[4].string)
                player_statistics[player_name]['excitement_index'] = excitement_index
            except ValueError:
                player_statistics[player_name]['excitement_index'] = 0.0

            # comeback factor
            try:
                comeback_factor = float(career_stats[5].string)
                player_statistics[player_name]['comeback_factor'] = comeback_factor
            except ValueError:
                player_statistics[player_name]['comeback_factor'] = 0.0

            # deuce court ace %
            try:
                deuce_ace_percentage = float(career_stats[6].string[:-1])
                player_statistics[player_name]['deuce_ace_percentage'] = deuce_ace_percentage
            except ValueError:
                player_statistics[player_name]['deuce_ace_percentage'] = 0.0

            # deuce court service point won %
            try:
                deuce_serves_won_percentage = float(career_stats[7].string[:-1])
                player_statistics[player_name]['deuce_service_point_won_percentage'] = deuce_serves_won_percentage
            except ValueError:
                player_statistics[player_name]['deuce_service_point_won_percentage'] = 0.0

            # ad court ace %
            try:
                ad_ace_percentage = float(career_stats[8].string[:-1])
                player_statistics[player_name]['ad_ace_percentage'] = ad_ace_percentage
            except ValueError:
                player_statistics[player_name]['ad_ace_percentage'] = 0.0

            # ad court service point won %
            try:
                ad_serves_won_percentage = float(career_stats[9].string[:-1])
                player_statistics[player_name]['ad_service_point_won_percentage'] = ad_serves_won_percentage
            except ValueError:
                player_statistics[player_name]['ad_service_point_won_percentage'] = 0.0

            # deuce court return point won %
            try:
                deuce_returns_won_percentage = float(career_stats[10].string[:-1])
                player_statistics[player_name]['deuce_return_point_won_percentage'] = deuce_returns_won_percentage
            except ValueError:
                player_statistics[player_name]['deuce_return_point_won_percentage'] = 0.0

            # ad court return point won %
            try:
                ad_returns_won_percentage = float(career_stats[11].string[:-1])
                player_statistics[player_name]['ad_return_point_won_percentage'] = ad_returns_won_percentage
            except ValueError:
                player_statistics[player_name]['ad_return_point_won_percentage'] = 0.0
        except TypeError as e:
            print(f"Stats not found for player {player_name}")
            not_found.append(player_name)

        num_processed += 1
        print(str(round((num_processed/num_players)*100, 3)) + "%")

    print(f"{len(player_statistics.keys()) - len(not_found)} players' statistics have been parsed")
    print(f"{len(not_found)} players could not be found: {not_found}")
    return player_statistics

def build_dataframe(stats_dict: dict):
    stats_list = list(list(stats_dict.items())[0][1].keys())
    data = {}
    num_updates_completed = 0
    # add parsed stats as columns to data frame
    winner_col = []
    winner_name_col = []
    loser_name_col = []
    for i in range(0, matches.shape[0]):
        winner_col.append(random.randint(1,2))
        winner_name_col.append(matches.at[i, 'winner_name'])
        loser_name_col.append(matches.at[i, 'loser_name'])
    data['winner'] = winner_col
    data['winner_name'] = winner_name_col
    data['loser_name'] = loser_name_col
    for stat in stats_list:
        p1_col = []
        p2_col = []
        for i in range(0, matches.shape[0]):
            winner_name = matches.at[i, 'winner_name']
            loser_name = matches.at[i, 'loser_name']
            winner_key = winner_col[i]
            try:
                if winner_key == 1:
                    p1_col.append(stats_dict[winner_name][stat])
                else:
                    p2_col.append(stats_dict[winner_name][stat])
            except KeyError as e:
                if winner_key == 1:
                    p1_col.append(0.0)
                else:
                    p2_col.append(0.0)
            try:
                if winner_key == 1:
                    p2_col.append(stats_dict[loser_name][stat])
                else:
                    p1_col.append(stats_dict[loser_name][stat])
            except KeyError as e:
                if winner_key == 1:
                    p2_col.append(0.0)
                else:
                    p1_col.append(0.0)
        data[f"p1_{stat}"] = p1_col
        data[f"p2_{stat}"] = p2_col
        num_updates_completed += 1
        print(f"Building data frame: {round((num_updates_completed/len(stats_list))*100, 3)}%")
    return pd.DataFrame(data=data)

if __name__ == "__main__":
    stats_dict = compile_statistics()
    data_frame = build_dataframe(stats_dict)
    data_frame.to_csv(output_filename, encoding='utf-8', index=False)
