#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: chenjinqian
# email: 2012chenjinqian@gmail.com


import os
import pickle
import random


def main():
    pass


class guess_four(object):

    def __init__(self):
        self.rule_d = self.prepare_rule_d()

        self.refresh_game()

    def prepare_number_d(self):
        """
        return dict of possible numbers, like {1234:True, 1246:True, ...}
        """
        base = [int(i) for i in range(10)]
        rlt_d = {}
        for a in base:
            for b in base:
                for c in base:
                    for d in base:
                        test_dup_set = set([a, b, c, d])
                        if len(test_dup_set) == 4:
                            num_one = a*1000 + b*100 + c*10 + d
                            rlt_d[num_one] = True
        return rlt_d

    def prepare_rule_d(self):
        """
        a --> 8
        b --> 1
        c --> 0
        a1b2 --> 8+2=10
        return nested dict as rule,
        like {1234:{1234:32, 4321:4, ...}, {1235:{...}...}...}
        """
        rule_d_fp = "./rule_d.dump"
        if os.path.exists(rule_d_fp):
            rule_d = pickle.load(open(rule_d_fp, "rb"))
            return rule_d
        rlt_d = {}
        guess_level = self.prepare_number_d()
        target_level = self.prepare_number_d()
        for g in guess_level:
            if g not in rlt_d:
                rlt_d[g] = {}
            for t in target_level:
                rlt_d[g][t] = self.evalue_a_guess(g, t)
        pickle.dump(open(rule_d_fp, "wb"))
        return rlt_d

    def evalue_a_guess(self, guess, target):
        g_l = self.decomp(guess)
        t_l = self.decomp(target)
        have_in = 0
        same_place = 0
        for g in g_l:
            for t in t_l:
                if g == t:
                    have_in += 1
        for g, t in zip(g_l, t_l):
            if g == t:
                same_place += 1
        rlt = same_place * 8 + (have_in - same_place)
        return rlt

    def decomp(self, num, n=4):
        num = int(num)
        tmp_list = []
        while num > 0:
            a = num % 10
            tmp_list.append(a)
            num = (num - a) / 10
        if n is not None:
            l_tmp = len(tmp_list)
            while l_tmp < n:
                tmp_list.append(int(0))
                l_tmp += 1
        rlt_list = [int(i) for i in tmp_list]
        # for i in tmp_list:
        #     rlt_list = [int(i)] + rlt_list
        return rlt_list

    def display_eval(self, value):
        rlt = []
        while value >= 8:
            value -= 8
            rlt.append("A")
        while value >= 1:
            value -= 1
            rlt.append("B")
        return "".join(rlt)

    def make_guess(self,
                     status_d=None,
                     rule_d=None):
        """
        return best guess next step, and maxmum uncertainlity,
        as a dictionary.
        """
        if status_d is None:
            status_d = self.status_d
        if rule_d is None:
            rule_d = self.rule_d
        # guess_cnt_min = None
        # rlt_guess = None
        guess_cnt_min = 5040
        for guess in status_d:
            cnt_d = {}
            for target in status_d:
                code = rule_d[guess][target]
                if code not in cnt_d:
                    cnt_d[code] = 1
                else:
                    cnt_d[code] += 1
                guess_cnt = max([cnt_d[i] for i in cnt_d])
                # if guess_cnt_min is None:
                #     guess_cnt_min = guess_cnt
                #     rlt_guess = guess
            if guess_cnt < guess_cnt_min:
                guess_cnt_min = guess_cnt
                rlt_guess = guess
        for guess in rule_d:
            if guess in status_d:
                continue
            cnt_d = {}
            for target in status_d:
                code = rule_d[guess][target]
                if code not in cnt_d:
                    cnt_d[code] = 1
                else:
                    cnt_d[code] += 1
                guess_cnt = max([cnt_d[i] for i in cnt_d])
                # if guess_cnt_min is None:
                #     guess_cnt_min = guess_cnt
                #     rlt_guess = guess
            if guess_cnt < guess_cnt_min:
                guess_cnt_min = guess_cnt
                rlt_guess = guess
        rlt = {}
        rlt[rlt_guess] = guess_cnt_min
        return rlt

    def feed_back(self,
                        guess,
                        feed_back,
                        status_d=None,
                        rule_d=None,
                        persudo=False):
        feed_code = self.code_feed_back(feed_back)
        if status_d is None:
            status_d = self.status_d
        if rule_d is None:
            rule_d = self.rule_d
        new_status_d = {}
        for k in status_d:
            if rule_d[k][guess] == feed_code:
                new_status_d[k] = True
                # should not change dictionary during iteration
        if not persudo:
            self.status_d = new_status_d
        return new_status_d

    def code_feed_back(self, feed_back):
        assert(type(feed_back)) == str
        rlt = 0
        for i in feed_back:
            if i == "A" or i == "a":
                rlt += 8
            if i == "B" or i == "b":
                rlt += 1
        return rlt

    def process(self, ):
        pass

    def server(self, guess_input):
        if self.answer is None:
            print("Not prepared one answer. Please use self.refresh_game to start.")
            return None
        rlt_show = self.display_eval(self.evalue_a_guess(guess_input, self.answer))
        self.guess_history.append(guess_input)
        self.feed_back_history.append(rlt_show)
        return rlt_show

    def refresh_game(self):
        self.guess_history = []
        self.feed_back_history = []
        self.ai_guess_history = []
        self.ai_feed_back_history = []
        self.status_d = self.prepare_number_d()
        self.answer = random.sample([i for i in self.rule_d], 1)[0]
        return True

    def show_answer(self):
        return self.answer

    def show_history():
        rlt = [i for i in zip(self.guess_history, self.feed_back_history)]


if __name__ == "__main__":
    main()
