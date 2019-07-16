#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: chenjinqian
# email: 2012chenjinqian@gmail.com


import random


class gmb(object):
    def __init__(self, chance=0.5, r1=2, r2=-1, asset=100, cnt=0):
        "kelly fomula"
        self.chance = chance
        self.r1 = 2
        self.r2 = -1
        self.asset = asset
        self.cnt = 0
        pass

    def bet_1(self, n, v=True):
        assert(0 < n <= self.asset)
        # self.cnt += 1
        self.cnt = self.cnt + 1
        print("bet:%s"%(n))
        rlt = self.roll()
        if rlt:
            gain = self.r1 * n
            if v:
                print("win:%s"%(gain))
        else:
            gain = self.r2 * n
            if v:
                print("loss:%s"%(n))
        print("count: %s"%(self.cnt))
        rlt = self.asset + gain
        self.asset = rlt
        return rlt  # emacs

    def bet_2(self, n, v=True):
        """
        exponent bet
        1,2,4,8,16
        """
        keep_rolling = True
        roll_rlt = []
        while keep_rolling:
            rlt_one = self.roll()
            if rlt_one:
                roll_rlt.append(rlt_one)
            else:
                keep_rolling = False
        if len(roll_rlt):
            gain = pow(2, len(roll_rlt) - 1)
        else:
            gain = 0
        if v:
            print("gain %s"%(gain))
        self.asset = self.asset + gain - n
        rlt = gain - n
        return rlt

    def bet_3(self):
        """
        double bet
        """
        pass



    def roll(self):
        dice = random.random()
        return bool(self.chance > dice)

    def percent(self, n):
        assert(0 < n <= 100)
        return self.asset * n / 100

    def cbet(self, n, x):
        for i in range(x):
            rlt = self.bet(self.percent(n))
        return rlt
