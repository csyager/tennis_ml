import sys
from bs4 import BeautifulSoup
import requests
import re
import joblib

def get_target_stats(player_names: list):
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

    stats_list = [[], []]
    for i in range(len(player_names)):
        request_url = url + player_names[i].replace(" ", "") + ".js"
        response = requests.get(request_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find("table", id="pbp-stats")
        career_stats = table("tr")[-1]("td")

        matches_played = int(re.search("\((.*?)\)", career_stats[0].string).group(1).split()[0])
        stats_list[i].append(matches_played)

        blr = float(career_stats[2].string)
        stats_list[i].append(blr)

        dr_plus = float(career_stats[3].string)
        stats_list[i].append(dr_plus)

        excitement_index = float(career_stats[4].string)
        stats_list[i].append(excitement_index)

        comeback_factor = float(career_stats[5].string)
        stats_list[i].append(comeback_factor)

        deuce_ace_percentage = float(career_stats[6].string[:-1])
        stats_list[i].append(deuce_ace_percentage)

        deuce_serves_won_percentage = float(career_stats[7].string[:-1])
        stats_list[i].append(deuce_serves_won_percentage)

        ad_ace_percentage = float(career_stats[8].string[:-1])
        stats_list[i].append(ad_ace_percentage)

        ad_serves_won_percentage = float(career_stats[9].string[:-1])
        stats_list[i].append(ad_serves_won_percentage)

        deuce_returns_won_percentage = float(career_stats[10].string[:-1])
        stats_list[i].append(deuce_returns_won_percentage)

        ad_returns_won_percentage = float(career_stats[11].string[:-1])
        stats_list[i].append(ad_returns_won_percentage)

    return [val for pair in zip(stats_list[0], stats_list[1]) for val in pair]

# load trained model
clf = joblib.load(sys.argv[1])

target_stats = get_target_stats([sys.argv[2], sys.argv[3]])
predicted_winner_number = clf.predict([target_stats])[0]
print(predicted_winner_number)
