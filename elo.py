#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys

'''
计算A对B的胜率期望值
公式里的常数默认取10和400
'''
def E(rankA, rankB, base = 10, power = 400):
    return 1 / ( 1 + pow(base, (1.0 * (rankB - rankA) / power)))   

'''
计算A对阵B后，新的rank分数
'''
def R(oldRankA, oldRankB, scoreA, k = 32, base = 10, power = 400):
    if (scoreA not in [0, 0.5, 1]):
        raise ValueError("Invalid score!", scoreA)
    e = E(oldRankA, oldRankB, base, power)
    return oldRankA + k * (scoreA - e)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "usage: %s rankA rankB scoreA" % sys.argv[0]
    else:
        rankA = float(sys.argv[1])
        rankB = float(sys.argv[2])
        scoreA = float(sys.argv[3])
        scoreB = 1 - scoreA

        newRankA = R(rankA, rankB, scoreA)
        newRankB = R(rankB, rankA, scoreB)

        print "Ea %.2f, Eb %.2f" % (E(rankA, rankB), E(rankB, rankA))

        print "A rank: %.2f -> %.2f" % (rankA, newRankA)
        print "B rank: %.2f -> %.2f" % (rankB, newRankB)
