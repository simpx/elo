#!/usr/bin/env python
# -*- coding: utf8 -*-
import pprint
import elo

pp = pprint.PrettyPrinter(indent=4)

# 解析后的数据
parsed_league = {}
parsed_teams = {}
parsed_games = []
ranks = {}

'''
find_between("adfl[a[b]c]dfkjl", "[", "]") -> "[a[b]c]"
'''
def find_between(string, from_str, to_str):
    return string[string.index(from_str): string.rindex(to_str) + 1]

def team_name(team_id):
    return parsed_teams[team_id]["name"]

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
            first_half_host_score, first_half_guest_score = [int(x) for x in game[6].split('-')]
            second_half_host_score, second_half_guest_score = [int(x) for x in game[6].split('-')]
            host_score = first_half_host_score + second_half_host_score
            guest_score = first_half_guest_score + second_half_guest_score
            result = 0.5
            if host_score > guest_score:
                result = 1
            elif host_score < guest_score:
                result = 0
            data = {"host_id": game[4], "guest_id": game[5],
                    "host_score": host_score, "guest_score": guest_score,
                    "first_half_host_score": first_half_host_score,
                    "first_half_guest_score": first_half_guest_score,
                    "second_half_host_score": second_half_host_score,
                    "second_half_guest_score": second_half_guest_score,
                    "round": idx + 1, "result": result}
            parsed_games.append(data)
            
# 展示所有数据

'''
print "***************"
print "league: "
pp.pprint(parsed_league)
print "***************"
print "team: "
pp.pprint(parsed_teams)
print "***************"
print "games: "
pp.pprint(parsed_games)
'''

#############################

print "%d games parsed" % len(parsed_games)

for game in parsed_games:
    host_id = game["host_id"]
    guest_id = game["guest_id"]
    host_name = team_name(host_id)
    guest_name = team_name(guest_id)
    host_old_rank = ranks.get(host_id, 1000)
    guest_old_rank = ranks.get(guest_id, 1000)
    host_score = game["host_score"]
    guest_score = game["guest_score"]

    if host_score > guest_score:
        host_result = 1
    elif host_score == guest_score:
        host_result = 0.5
    else:
        host_result = 0
    guest_result = 1 - host_result
    host_new_rank = elo.R(host_old_rank, guest_old_rank, host_result)
    guest_new_rank = elo.R(guest_old_rank, host_old_rank, guest_result)
    ranks[host_id] = host_new_rank 
    ranks[guest_id] = guest_new_rank 
    print "%s(%.2f) %d:%d %s(%.2f) -> (%.2f) (%.2f)" % (host_name, host_old_rank,
                                                host_score, guest_score,
                                                guest_name, guest_old_rank,
                                                host_new_rank, guest_new_rank)
