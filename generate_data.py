#!/usr/bin/env python
# -*- coding: utf8 -*-
import pprint

pp = pprint.PrettyPrinter(indent=4)

'''
find_between("adfl[a[b]c]dfkjl", "[", "]") -> "[a[b]c]"
'''
def find_between(string, from_str, to_str):
    return string[string.index(from_str): string.rindex(to_str) + 1]

# 解析后的数据
parsed_league = {}
parsed_teams = {}
parsed_games = []

# 解析联赛数据
file_data = open("s36.js").readlines()
data_league_str = find_between(file_data[0], '[', ']')
data_league = eval(data_league_str)
parsed_league['name'] = data_league[1]

# 解析队伍数据
data_teams_str = find_between(file_data[1], '[', ']')
data_teams = eval(data_teams_str)
for team in data_teams:
    parsed_teams[team[0]] = {"name": team[1], "eng": team[3]}

x = 0
# 解析赛事数据
for i in range(2, 2 + 38):
    if not file_data[i].strip().startswith("jh[\"R_%d\"" % (i - 1)):
        print "should starts with %s , but: %s" % ( ("jh[\"R_%d\"" % (i - 1)), file_data[i])
        sys.exit(-1)
    round_str = file_data[i].strip().split(' ', 2)[2][:-1]
    round_str = round_str.replace(",,,", ",'x','x',", -1).replace(",,", ",'x',", -1)
    round_ = eval(round_str)
    for idx in range(len(round_)):
        game = round_[idx]
        if game[2] == -1:
            first_half_score_host, first_half_score_guest = [int(x) for x in game[6].split('-')]
            second_half_score_host, second_half_score_guest = [int(x) for x in game[6].split('-')]
            score_host = first_half_score_host + second_half_score_host
            score_guest = first_half_score_guest + second_half_score_guest
            result = 0.5
            if score_host > score_guest:
                result = 1
            elif score_host < score_guest:
                result = 0
            data = {"host_id": game[4], "guest_id": game[5],
                    "score_host": score_host, "score_guest": score_guest,
                    "first_half_score_host": first_half_score_host,
                    "first_half_score_guest": first_half_score_guest,
                    "second_half_score_host": second_half_score_host,
                    "second_half_score_guest": second_half_score_guest,
                    "round": idx + 1, "result": result}
            parsed_games.append(data)
            
# 展示所有数据

print "***************"
print "league: "
pp.pprint(parsed_league)
print "***************"
print "team: "
pp.pprint(parsed_teams)
print "***************"
print "games: "
pp.pprint(parsed_games)
