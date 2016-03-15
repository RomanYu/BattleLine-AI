#!/usr/bin/python

import sys
import os

if __name__ == '__main__':
    cards_in_hands = []
    status = [[] for i in range(9)]
    
    while True:
        n = int(sys.stdin.readline())
        #sys.stderr.write("demo %d n: %d\n" % (os.getpid(), n))
        over = False
        for i in range(n):
            cmd = sys.stdin.readline()
            #sys.stderr.write("demo %d cmd: " % os.getpid()+ cmd)
            items = cmd.split()
            if items[0] == 'cardget':
                cards_in_hands.append(items[1])
            elif items[0] == 'rival':
                pass
            else:
                over = True
        if over:
            break
        else:
            for i in range(9):
                if len(status[i]) < 3:
                    region = i
                    status[i].append(cards_in_hands[0])
                    break
            sys.stdout.write("act %d %s\n" % (region, cards_in_hands[0]))
            sys.stdout.flush()
            cards_in_hands = cards_in_hands[1:]
