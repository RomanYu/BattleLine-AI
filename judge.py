#!/usr/bin/python

import sys
import json
import random
from subprocess import PIPE, Popen

class Cardpool(object):
    def __init__(self):
        self.cards = []
        for c in range(6):
            for i in range(1, 11):
                card = "%c%d" % (chr(ord('A') + c), i)
                self.cards.append(card)
        random.shuffle(self.cards)
        
        self.used_cnt = 0

    def has_next(self):
        return self.used_cnt < 60

    def get_next(self):
        card = self.cards[self.used_cnt]
        self.used_cnt += 1
        return card

cardpool = Cardpool()

class Status(object):
    def __init__(self):
        self.regions_0 = [[] for i in range(9)]
        self.regions_1 = [[] for i in range(9)]
        self.first_full = [-1] * 9
        self.region_status = [-1] * 9
        self.game_status = -1
        self.showed_cards = set()

    def putcard(self, player, region, card):
        if player == 0:
            self.regions_0[region].append(card)
            if self.first_full[region] == -1 and len(self.regions_0[region]) == 3:
                self.first_full[region] = 0
        else:
            self.regions_1[region].append(card)
            if self.first_full[region] == -1 and len(self.regions_1[region]) == 3:
                self.first_full[region] = 1
            
        self.showed_cards.add(card)
        self.update()


    def compose_wedge(self, region):
        for c in range(6):
            for i in range(10, 2, -1):
                valid = True
                cards = ['%c%d' % (chr(ord('A') + c), i-j) for j in range(3)]
                for card in cards:
                    if card not in self.showed_cards and card not in region:
                        valid = False
                        break
                if valid:
                    return cards
        return None

    def compose_phalanx(self, region):
        for i in range(10, 0, -1):
            cards = ['%c%d' % (chr(ord('A') + c), i) for c in range(6)]
            valid = True
            for card in region:
                if card not in cards:
                    valid = False
                    break
            if not valid:
                continue
            cnt = 0
            for card in cards:
                if card not in self.showed_cards:
                    cnt += 1
            if len(region) + cnt >= 3:
                r = [card for card in region]
                for card in cards:
                    if card not in self.showed_cards:
                        r.append(card)
                        if len(r) == 3:
                            break
                return r
        return None

    def compose_battalion(self, region):
        r = None
        for c in range(6):
            valid = True
            for card in region:
                if card[0] != chr(ord('A') + c):
                    valid = False
                    break
            if valid:
                rc = [card for card in region]
                for i in range(10, 0, -1):
                    card = '%c%d' % (chr(ord('A') + c), i)
                    if card not in self.showed_cards:
                        rc.append(card)
                        if len(rc) == 3:
                            break
                if len(rc) == 3:
                    if not r or self.judge_region(rc, r) == 0:
                        r = rc
        return r

    def is_skirmish(self, card1, card2, card3):
        numbers = [int(card1[1:]), int(card2[1:]), int(card3[1:])]
        numbers.sort()
        return numbers[1] - numbers[0] == 1 and numbers[2] - numbers[0] == 2

    def compose_skirmish(self, region):
        cards_remain = []
        r = None
        for c in range(6):
            for i in range(10):
                card = '%c%d' % (chr(ord('A') + c), i)
                if card not in self.showed_cards:
                    cards_remain.append(card)

        if len(region) == 2:
            for card in cards_remain:
                if self.is_skirmish(region[0], region[1], card):
                    rc = [region[0], region[1], card]
                    if not r or self.judge_region(rc, r) == 0:
                        r = rc
        elif len(region) == 1:
            for card1 in cards_remain:
                for card2 in cards_remain:
                    if card1 != card2:
                        if self.is_skirmish(region[0], card1, card2):
                            rc = [region[0], card1, card2]
                            if not r or self.judge_region(rc, r) == 0:
                                r = rc
        else:
            for card1 in cards_remain:
                for card2 in cards_remain:
                    if card1 != card2:
                        for card3 in cards_remain:
                            if card3 != card1 and card3 != card2:
                                if self.is_skirmish(card1, card2, card3):
                                    rc = [card1, card2, card3]
                                    if not r or self.judge_region(rc, r) == 0:
                                        r = rc
        return r

    def compose_host(self, region):
        r = [card for card in region]
        for i in range(10, 0, -1):
            if len(r) == 3:
                break
            for c in range(6):
                card = '%c%d' % (chr(ord('A') + c), i)
                if card not in self.showed_cards:
                    r.append(card)
                    if len(r) == 3:
                        break
        assert(len(r) == 3)
        return r
            
    def guess_max(self, region):
        for fun in [self.compose_wedge, self.compose_phalanx, self.compose_battalion, self.compose_skirmish, self.compose_host]:
            r = fun(region)
            if r:
                return r

    def judge_level(self, r):
        same_color = (r[0][0] == r[1][0] and r[0][0] == r[2][0])
        numbers = [int(card[1:]) for card in r]
        numbers.sort()
        order_numbers = (numbers[1] - numbers[0] == 1 and numbers[2] - numbers[0] == 2)
        same_numbers = (numbers[0] == numbers[1] and numbers[0] == numbers[2])
        if same_color and order_numbers:
            return 5
        elif same_numbers:
            return 4
        elif same_color:
            return 3
        elif order_numbers:
            return 2
        else:
            return 1

    def judge_sum(self, r0, r1, n):
        c0 = 0
        c1 = 0
        for card in r0:
            c0 += int(card[1:])
        for card in r1:
            c1 += int(card[1:])
        if c0 > c1:
            return 0
        elif c1 > c0:
            return 1
        elif n != -1:
            return self.first_full[n]
        else:
            return -1

    def judge_region(self, r0, r1, n = -1):
        level0 = self.judge_level(r0)
        level1 = self.judge_level(r1)
        if level0 < level1:
            return 1
        elif level0 > level1:
            return 0
        else:
            return self.judge_sum(r0, r1, n)

    def update_region(self, n):
        r0 = self.regions_0[n]
        r1 = self.regions_1[n]
        #print r0, r1

        if len(r0) + len(r1) == 6:
            self.region_status[n] = self.judge_region(r0, r1, n)
        else:
            if len(r0) == 3:
                rg1 = self.guess_max(r1)
                r = self.judge_region(r0, rg1)
                if r == 0:
                    self.region_status[n] = 0
            if len(r1) == 3:
                rg0 = self.guess_max(r0)
                r = self.judge_region(rg0, r1)
                if r == 1:
                    self.region_status[n] = 1

    def update(self):
        for i in range(9):
            pre_status = self.region_status[i]
            self.update_region(i)
            if self.region_status[i] != pre_status:
                output_command(command='region_win', player=self.region_status[i], region=str(i))

        #print self.region_status
        #print self.first_full
        sum_0 = 0
        sum_1 = 0
        for i in range(9):
            if self.region_status[i] == 0:
                sum_0 += 1
            if self.region_status[i] == 1:
                sum_1 += 1
            if i > 6:
                continue
            if self.region_status[i] == 0 and self.region_status[i+1] == 0 and self.region_status[i+2] == 0:
                self.game_status = 0
                return
            if self.region_status[i] == 1 and self.region_status[i+1] == 1 and self.region_status[i+2] == 1:
                self.game_status = 1
                return
        if sum_0 >= 5:
            self.game_status = 0
        if sum_1 >= 5:
            self.game_status = 1


def output_command(**kw):
    #print {'command':command, 'player':player, 'card':card}
    print str(kw) + ','

class Player(object):
    def __init__(self, n):
        player_key = 'player%d'%n
        config = json.load(open("config.json"))
        app = config[player_key]
        self.cards_in_hand = set()
        self.msg = []
        self.n = n

        p = Popen(app, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
        (self.child_stdin, self.child_stdout) = (p.stdin, p.stdout)
        

    def end_game(self, is_win):
        if is_win:
            self.msg.append("youwin")
        else:
            self.msg.append("youlose")
        self.send_msg()

    def send_msg(self):
        self.child_stdin.write("%d\n" % len(self.msg))
        for m in self.msg:
            self.child_stdin.write("%s\n" % m)
        self.child_stdin.flush()
        self.msg = []

    def receive_msg(self):
        line = self.child_stdout.readline()
        return line

    def interact(self):
        self.send_msg()
        line = self.receive_msg()
        items = line.split()
        assert(items[0] == "act")
        return (int(items[1]), items[2])

    def process(self):
        #print self.cards_in_hand
        while len(self.cards_in_hand) < 7 and cardpool.has_next():
            card = cardpool.get_next()
            output_command(command='get_card', player=str(self.n), card=card)
            self.cards_in_hand.add(card)
            self.msg.append("cardget " + card)
        (region, card) = self.interact()
        output_command(command='action', player=str(self.n), region=region, card=card)
        self.cards_in_hand.remove(card)
        return region, card

    def update_rival(self, region, card):
        self.msg.append("rival %d %s" % (region, card))

status = Status()
    
class Game(object):
    def __init__(self):
        #magic control who's on the offensive 
        #magic = random.randint(0,1)
        magic = 0
        self.players = [Player(magic), Player(1-magic)]

    def start(self):
        round_cnt = 0
        while status.game_status == -1:
            #print "round %d" % round_cnt
            round_cnt += 1
            for i in range(0, 2):
                (region, card) = self.players[i].process()
                status.putcard(i, region, card)
                self.players[1-i].update_rival(region, card)
                
                if status.game_status > -1:
                    break
        self.players[0].end_game(status.game_status == 0)
        self.players[1].end_game(status.game_status == 1)
        #if status.game_status == 0:
        #    print 'player0 win'
        #else:
        #    print 'player1 win'
        output_command(command="game_win", player=str(status.game_status))

if __name__ == '__main__':
    Game().start()
