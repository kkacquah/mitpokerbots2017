# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 22:18:42 2017

@author: henoch
"""
from deuces import Card
from deuces import Evaluator
from deuces import Deck
from random import shuffle

data = dict()
data['prob'] = 0.0
data['deck'] = []
data['score'] = 0

def getAction(myHand,boardCards,legalActions,lastActions,history,switched):

    board = []
    for card in boardCards:
        board.append(Card.new(card))
    hand = [Card.new(myHand[0]),Card.new(myHand[1])]

    deck = data.get('deck',[])
    if len(deck) <= 1:
        fillDeck(board,hand)

    Eval = Evaluator()
    score = Eval.evaluate(board, hand)
    print 'Score is ' + str(score)
    data['score'] = score
    #name = Eval.class_to_string(score) #if we want to know what it's called 'Straight'

    if switched or hasAction("DEAL",lastActions) or len(boardCards) <= 3 or data.get('prob',0.0) == 0.0: #new cards added or hand switched
        if switched:
            updateDeck(hand,board)
        probabilityOfWin(hand,board,score,Eval)
    
    prob = data.get('prob',0.0)
    print 'prob det as ' + str(prob)
    if hasAction("DISCARD",legalActions): #means at flop or turn and can discard card
        scores = checkMyOdds(board,hand,Eval)
        print 'I have discard option my score is ' + str(score)
        print 'Averages are ' + str(scores)
        goFor = choose([score]+scores)
        print 'so I choose' + str(goFor)
        
        if goFor == 0:
            return 'CHECK\n'
        else:
            return 'DISCARD:'+myHand[goFor - 1]

    elif not hasAction("CHECK",legalActions):  #means the person has bet #assume BET, RAISE,CALL,FOLD
        print 'cp 1'

        if prob < 30:
            print 'cp 2'
            if len(boardCards)>3: #on turn or river - no more chances to discard
                return 'FOLD\n' #We're not going to win

            else: #on flop -> one more time to discard
                print 'cp 4'
                scores = checkMyOdds(board,hand,Eval)
                print 'average score can be' + str(scores)
                if (score - scores[2]) < 400: #average change by switching is low
                    return 'FOLD\n'

        if prob > 60 :
            print 'cp 3'
            if prob > 80:
                print 'My odds GREAT'
                return 'RAISE:#\n' # must fix with amount to raise

            scores = checkMyOdds(board,hand,Eval)
            print 'cp 5'
            print 'average score can be' + str(scores)
            if (score - scores[2]) > 200: #one more card will give even better chance
                return 'RAISE\n'

        return 'CALL\n'


    else: # assume normal BET, CHECK
        print 'cp 6'
        if prob > 65:
            print 'cp 7'
            return 'BET:#\n' #fix later

        return 'CHECK\n'

def hasAction(act,actions):
    print "possibile actions are" + str(actions)
    for action in actions:
        print "this action is" + str(action)
        if action.find(act) != -1:
            print "has wanted act"
            return True
    return False

def checkMyOdds(board,hand,Eval):
    deck = list(data.get("deck",fillDeck(board,hand)))
    shuffle(deck)

    firstAverage = getAverage(0,deck[:],hand,board,Eval)
    secondAverage = getAverage(1,deck[:],hand,board,Eval)
    switchScore = (firstAverage + secondAverage) / 2

    return [firstAverage,secondAverage,switchScore]
def choose(scores):
    currentScore = scores[0]
    firstAverage = scores[1]
    secondAverage = scores[2]

    if currentScore >= firstAverage:
        if currentScore >= secondAverage:
            return 0 #current largest (or equal)
        else:
            return 2 #removing second gives best odds
    else:
        if firstAverage >= secondAverage:
            return 1 #remove first is the best
        else:
            return 2 #remove second is the best

def getAverage(index,deck,hand,board,Eval):
    total = 0
    count = 0
    while len(deck) > 0:
        newCard = deck.pop(0)
        testHand = hand[:]
        testHand[index] = newCard
        newScore = Eval.evaluate(board, testHand)
        total += newScore
        count += 1

    return total / float(count)

def probabilityOfWin(hand,board,score,Eval):
    deck = data.get("deck",fillDeck(board,hand)) #get already made deck or new
    shuffle(deck)
    possibilities = (50-len(board))*(49-len(board))
    count = 0

    for i in range(0,len(deck)-1):
        for j in range(i+1,len(deck)):
            testHand = [deck[i],deck[j]]
            newScore = Eval.evaluate(board, testHand)
            if score < newScore:
                count +=1 #would win against random hand

    prob = float(count)*100/possibilities
    data['prob'] = prob
    #print 'Probability is' + str(prob)
    return prob

def fillDeck(board,hand):
    d = Deck()
    deck = d.GetFullDeck() #empty list for some reason - FIX!
    #print deck
    shuffle(deck)

    #print deck

    for card in hand:
        if card in deck: #make sure card hasn't been removed
            deck.remove(card)

    for card in board:
        if card in deck: #make sure card hasn't been removed
            deck.remove(card)

    data['deck'] = deck
    return deck


def updateDeck(hand,board):
    deck = data.get('deck',[])

    if len(deck) <=1:
        deck = fillDeck(hand,board)

    for card in hand:
        if card in deck: #make sure card hasn't been removed
            deck.remove(card)






