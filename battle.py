#!/usr/bin/python
####
## author : yao.yu, liangju.yu, ke.zhang, jackblack.zhang
####
import sys
import os
import copy
import itertools

# unkown_cards save the cards in rival's hand or in the cards heap
unkown_cards = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10',
                'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10',
                'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10',
                'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10',
                'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10',
                'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10',]

def get_combinations(cards, number):
    combinations = itertools.combinations(cards, number)
    return list(combinations)

def redefined_sort(card):
    card.sort()
    for i in card:
       if len(i) == 3:
            card.remove(i)
            card.append(i)
    return card

# get the type of three cards, input a list of three items, return a (type, number) tuple.
# 4 : Tong Hua Shun; 3: Zhadan; 2: Tong Hua; 1: Shun Zi; 0: None
def get_card_type(cards):
    color = []
    number = []
    temp_cards = copy.copy(cards)
    temp_cards = redefined_sort(temp_cards) 
    for card in temp_cards:
        color.append(card[0])
        number.append(int(card[1:])) 
    points = number[0] + number[1] + number[2]
    if number[0] == number[1] == number[2]:
        return 3, points
    is_same_color = color[0] == color[1] == color[2]
    is_num_strong_cont = number[0] + 1 == number[1] == number[2] - 1  
    temp = sorted(number)
    is_num_weak_cont = temp[0] + 1 == temp[1] == temp[2] - 1  
    if is_same_color and is_num_strong_cont:
        return 4, points
    elif is_same_color:
        return 2, points
    elif is_num_weak_cont:
        return 1, points
    else:
        return 0, points

# pk the cards of three cards, input two list of three items, return True (win) of False (lose).
def pk_cards(our, rival): 
    our_type, our_points = get_card_type(our)
    rival_type, rival_points = get_card_type(rival)
    if our_type == rival_type:
        if our_points > rival_points:
            return True
        else:
            return False
    elif our_type > rival_type:
        return True 
    else:
        return False

# predict the type of zero cards which can be composed a formation adding three new card, input a list of nothing, return a (type, number, (card_predicted)) tuple
def predict_zero_card_type(cards_in_region, other_cards_pairs):
    max_type = 0
    max_number = 0
    cards_predicted = None
    
    # iterate all the probable cards to find a max formation of cards.
    for cards_pair in other_cards_pairs:
        temp_cards_in_region = copy.copy(cards_in_region)
        temp_cards_in_region.extend(list(cards_pair))
        ret = get_card_type(temp_cards_in_region)
        if (ret[0] > max_type) or (ret[0] == max_type and ret[1] > max_number):
            cards_predicted = cards_pair
            (max_type, points) = ret  
   
    return max_type, points, cards_predicted

# predict the type of two cards which can be composed a formation adding a new card, input a list of two items, return a (type, number) tuple
def predict_one_card_type(cards_in_region, other_cards_pairs):
    max_type = 0
    max_number = 0
    cards_predicted = None

    # iterate all the probable cards to find a max formation of cards.
    for cards_pair in other_cards_pairs:
        temp_cards_in_region = copy.copy(cards_in_region)
        temp_cards_in_region.extend(list(cards_pair))
        ret = get_card_type(temp_cards_in_region)
        if (ret[0] > max_type) or (ret[0] == max_type and ret[1] > max_number):
            cards_predicted = cards_pair
            (max_type, points) = ret  

    return max_type, points, cards_predicted

# predict the type of two cards which can be composed a formation adding a new card, input a list of two items, return a (type, number) tuple
def predict_two_card_type(cards_in_region, other_cards):
    max_type = 0
    max_number = 0 
    card_predicted = None

    # iterate all the probable cards to find a max formation of cards.
    for card in other_cards:
        temp_cards_in_region = copy.copy(cards_in_region)
        temp_cards_in_region.append(card)
        ret = get_card_type(temp_cards_in_region)
        if (ret[0] > max_type) or (ret[0] == max_type and ret[1] > max_number):
            card_predicted = card
            (max_type, points) = ret
    
    return max_type, points, card_predicted 

# the strategy of card playing if there's two cards in the region.
# play the card if we can win in this region, else donnot play any card
def act_on_two_cards(cards_in_hands, our_cards_in_region, rival_cards_in_region, unkown_cards):
    temp_our_region = copy.copy(our_cards_in_region) 
    temp_rival_region = copy.copy(rival_cards_in_region) 

    our_max_type, our_points, our_card_predicted = predict_two_card_type(our_cards_in_region, cards_in_hands)
    temp_our_region.append(our_card_predicted)
    
    if len(rival_cards_in_region) == 3:
        rival_max_type, rival_points = get_card_type(rival_cards_in_region)
    else:
        if len(rival_cards_in_region) == 2:
            rival_max_type, rival_points, rival_card_predicted = predict_two_card_type(rival_cards_in_region, unkown_cards)
            temp_rival_region.append(rival_card_predicted)
        elif len(rival_cards_in_region) == 1:
            cards_pairs = get_combinations(unkown_cards, 2)
            rival_max_type, rival_points, rival_card_predicted = predict_one_card_type(rival_cards_in_region, cards_pairs)
            temp_rival_region.extend(rival_card_predicted)
        elif len(rival_cards_in_region) == 0:
            cards_pairs = get_combinations(unkown_cards, 3)
            rival_max_type, rival_points, rival_card_predicted = predict_zero_card_type(rival_cards_in_region, cards_pairs)
            temp_rival_region.extend(rival_card_predicted)
        else:
            #print 'there are some errors!'
            pass

# return the predicted card if we must win the pk, else return False
    if pk_cards(temp_our_region, temp_rival_region):
        return our_card_predicted
    else:
        return False
        #return rival_card_predicted

def act_on_two_cards_bad(cards_in_hands, status):
    region = None
    max_type = 0
    points = 0
    for i in range(len(status)):
        if len(status[i]) == 2:
            our_cards_in_region = status[i]
            our_max_type, our_points, our_card_predicted = predict_two_card_type(our_cards_in_region, cards_in_hands)
            if (our_max_type > max_type) or (our_max_type == max_type and our_points > points):
                region = i
                card_predicted = our_card_predicted 
                max_type = our_max_type
                points = our_points
    return region, card_predicted
###########


############

def max_number_card(cards_in_hands):
    max_number = -1
    my_card = False 
    for card in cards_in_hands:
        if int(card[1:]) > max_number:
            max_number = int(card[1:])
            my_card = card
    return my_card

def max_number_of_one_colortype(cards_in_hands):
    #print cards_in_hands
    color = []
    cardA = []
    cardB = []
    cardC = []
    cardD = []
    cardE = []
    cardF = []
    number = [0 for i in range(6)]
    for card in sorted(cards_in_hands):
        if card[0] == "A":
            number[0] += 1
            cardA.append(card)
        elif card[0] == "B":
            number[1] += 1
            cardB.append(card)
        elif card[0] == "C":
            number[2] += 1
            cardC.append(card)
        elif card[0] == "D":
            number[3] += 1
            cardD.append(card)
        elif card[0] == "E":
            number[4] += 1
            cardE.append(card)
        elif card[0] == "F":
            number[5] += 1;
            cardF.append(card)
    max = -1
    item = -1
    for index,val in enumerate(number):
        if val > max:
            max = val
            item = index
    #print item
    i = item
    if i == 0:
        redefined_sort(cardA)
        cardA.reverse()
        if int(cardA[0][1:]) > 5:
            return cardA[0]
        else:
            return max_number_card(cards_in_hands)
    elif i == 1:
        redefined_sort(cardB)
        cardB.reverse()
        if int(cardB[0][1]) > 5:
            return cardB[0]
        else:
            return max_number_card(cards_in_hands)
    elif i == 2:
        redefined_sort(cardC)
        cardC.reverse()
        if int(cardC[0][1]) > 5:
            return cardC[0]
        else:
            return max_number_card(cards_in_hands)
    elif i == 3:
        redefined_sort(cardD)
        cardD.reverse()
        if int(cardD[0][1]) > 5:
            return cardD[0]
        else:
            return max_number_card(cards_in_hands)
    elif i == 4:
        redefined_sort(cardE)
        cardE.reverse()
        if int(cardE[0][1]) > 5:
            return cardE[0]
        else:
            return max_number_card(cards_in_hands)
    elif i == 5:
        redefined_sort(cardF)
        cardF.reverse()
        if int(cardF[0][1]) > 5:
            return cardF[0]
        else:
            return max_number_card(cards_in_hands)

#def hastonghuashun():
#    return ""

#def haszhadan():
#    return ""
def verify_zhadan_init(cards_inhand):
    zhadan_list = []
    count = 0
    max_val=0
    max_card=0
    for i in range(len(cards_inhand)):
        card_cut = copy.copy(cards_inhand)
        card_cut.pop(i)
        count = 0
        for j in range(len(card_cut)):
            if int(card_cut[j][1:]) == int(cards_inhand[i][1:]):
                count = count+1
        if count > 2 or count ==2:
            zhadan_list.append(cards_inhand[i])
    if len(zhadan_list) >0:
		#print zhadan_list
        for card in zhadan_list:
            if int(card[1:]) > max_val:
                max_card=card
                max_val= int(card[1:])
        return max_card
    else:
        return False

def verify_tonghaushun_init(cards_inhand):
	tonghua_list=[]
	for i in range(len(cards_inhand)):
		card_cut = copy.copy(cards_inhand)
		card_cut.pop(i)
		if verify_tonghuashun_secondInput(card_cut, cards_inhand[i]) != False:
			tonghua_list.append(verify_tonghuashun_secondInput(card_cut, cards_inhand[i]))
	if len(tonghua_list) > 0:
		tonghua_list=redefined_sort(tonghua_list)
		return tonghua_list[-1]
	else:
		return False
 
def get_card_toput(mycard,cards_in_hands):
    value = verify_tonghaushun_init(cards_in_hands)
    if value != False:
        return value
    else:
        value = verify_zhadan_init(cards_in_hands)
        if value != False:
            return value
        else:
            return max_number_of_one_colortype(cards_in_hands);

 
def act_on_zero_cards(mycard,rivalcard,cards_in_hands,region):
    #loop to find whether rival has put one card.
    first = True
    for rival_region in rivalcard:
        if len(rival_region) > 0:
            first = False
            break
    #if not put , then I am the first
    if first == True:
        #sys.stderr.write('here')
        #sys.stdout.flush()
        #print("first");
        return 5,get_card_toput(mycard,cards_in_hands);
    else :
        # find place to put the card
        rivalplace = region
        while True:
            #judge whether there is space that no card is put
            if rivalplace < 8:
                rivalplace += 1
            else:
                rivalplace = 0;
            
            #sys.stderr.write('region:' + str(region) + '\n' + 'rivalplace' + str(rivalplace) +'\n')
            sys.stdout.flush()
            if rivalplace == region:
                if len(mycard[rivalplace]) == 0:
                    return rivalplace, get_card_toput(mycard,cards_in_hands);
                else:
                    return False
            #for the empty place we choose one card to put
#            for my_region in mycard:
            #sys.stderr.write('length:' + str(len(mycard[rivalplace])) + '\n')
            #sys.stdout.flush()
            elif len(mycard[rivalplace]) == 0:
                #return palce and value
                return rivalplace,get_card_toput(mycard,cards_in_hands);
                  
############

def verify_tonghuashun_secondInput(cardlist, card):
	color = card[0]
	number= int(card[1:])
	tonghuashun = []
	tonghuashun.append(card)
	for eachcard_in_hand in cardlist:
		if color != eachcard_in_hand[0]:
			continue
		if abs(number-int(eachcard_in_hand[1:])) > 2:
			continue
		tonghuashun.append(eachcard_in_hand)
	if len(tonghuashun) < 3:
		return False
	#tonghuashun = sorted(tonghuashun)
	tonghuashun =redefined_sort(tonghuashun)
	index = 0
	for x in tonghuashun:
		if int(x[1:]) == number:
			if index == 0:
				if int(tonghuashun[index+1][1:]) == number+1 and int(tonghuashun[index+2][1:]) == number +2:
					return tonghuashun[index+2]
				else:
					return False
			elif index == len(tonghuashun)-1:
				if int(tonghuashun[index-1][1:]) == number-1 and int(tonghuashun[index-2][1:]) == number-2:
					return tonghuashun[index-1]
			else:
				if int(tonghuashun[index-1][1:]) == number-1 and int(tonghuashun[index+1][1:]) == number+1:
					return tonghuashun[index+1]
		index = index + 1
	return False

def verify_zhadan_secondInput(cardlist, card):
	number= int(card[1:])
	zhadan = []
	zhadan.append(card)
	for eachcard_in_hand in cardlist:
		if int(eachcard_in_hand[1:]) == number:
			zhadan.append(eachcard_in_hand)
	if len(zhadan) < 3:
		return False
	return zhadan[1]

def samecolor_shunzi(cardlist,card):
    number = int(card[1:])
    color = card[0]
    for each in cardlist:
        if (each[0]==color and abs(int(each[1:])-number)<3):
            return each
    return False

def samecolor_max_val(cardlist,card):
    color = card[0]
    number = int(card[1:])
    max_val = 0
    for each in cardlist:
        if each[0] == color and int(each[1:]) > max_val:
             result =  each
             max_val = int(each[1:])
    if max_val > 5:
        return result
	return False

def verify_double_secondInput(cardlist,card):
	number = int(card[1:])
	for each in cardlist:
		if int(each[1:]) == number:
			return each
	return False

def verify_shunzi(cardlist, card):
	number = int(card[1:])
	for each in cardlist:
		if abs(number-int(each[1:])) < 2:
			return each
	return False

def vefify_sum(cardlist, card):
	ret = False
	number = int(card[1:])
	max_sum = 0
	for each in cardlist:
		if int(each[1:]) + number > max_sum:
			max_sum = int(each[1:])+number
			ret = each
	return ret

def act_on_one_cards(cards_in_hands,cards_in_region):
	card = cards_in_region[0]
	re1 = verify_tonghuashun_secondInput(cards_in_hands, card)
	if re1:
		return re1
	re2 = verify_zhadan_secondInput(cards_in_hands, card)
	if re2:
		return re2
	re3 = samecolor_shunzi(cards_in_hands,card)
	if re3:
		return re3
	return False

def act_on_one_cards_bad(cards_in_hands, status):
    region = -1
    for i in range(len(status)):
        if len(status[i]) == 1:
            region = i
            break
    if region == -1:
        return False
    card = status[i][0] 
    re = samecolor_max_val(cards_in_hands,card)
    if re:
        return region, re
    re4 = verify_double_secondInput(cards_in_hands,card)
    if re4:
		return region, re4
    re5 = verify_shunzi(cards_in_hands, card)
    if re5:
        return region, re5
    ret6 = vefify_sum(cards_in_hands, card)
    if ret6:
        return region, ret6

###########

if __name__ == '__main__':
    cards_in_hands = []
    status = [[] for i in range(9)]
    rival_status = [[] for i in range(9)]
    
    while True:
        n = int(sys.stdin.readline())
        #sys.stderr.write("demo %d n: %d\n" % (os.getpid(), n))
        over = False
        for i in range(n):
            cmd = sys.stdin.readline()
            #sys.stderr.write("demo %d cmd: " % os.getpid()+ cmd)
            items = cmd.split()
            last_rival_region = 4
            if items[0] == 'cardget':
                unkown_cards.remove(items[1])
                cards_in_hands.append(items[1])
            elif items[0] == 'rival':
                last_rival_region = int(items[1])
                card = items[2]
                unkown_cards.remove(card)
                rival_status[last_rival_region].append(card)
            else:
                over = True
        if over:
            break
        else:
            #sys.stderr.write(str(rival_status) + '\n')
            #sys.stdout.flush()
            for i in range(9):
                play_card = False
                region = i
                #sys.stderr.write(str(len(status[i])) + '\n')
                #sys.stdout.flush()
                if len(status[i]) >= 3:
                    continue
                elif len(status[i]) == 2:
                    play_card = act_on_two_cards(cards_in_hands, status[i], rival_status[i], unkown_cards) 
                    if play_card != False:
                        break
                elif len(status[i]) == 1:
                    play_card = act_on_one_cards(cards_in_hands, status[i]) 
                    if play_card != False:
                        break
            if play_card == False:
                ret = act_on_zero_cards(status, rival_status, cards_in_hands, last_rival_region) 
                if ret != False:
                    (region, play_card) = ret 
                    #sys.stderr.write(str(region))
                    #sys.stdout.flush()
            if play_card == False:
                ret = act_on_one_cards_bad(cards_in_hands, status) 
                if ret == False:
                    region, play_card = act_on_two_cards_bad(cards_in_hands, status)
                else:
                    (region, play_card) = ret
                #sys.stderr.write('error\n')
                #sys.stdout.flush()
            status[region].append(play_card)
            sys.stdout.write("act %d %s\n" % (region, play_card))
            sys.stdout.flush()
            #sys.stderr.write(str(status))
            #sys.stdout.flush()
            cards_in_hands.remove(play_card)
