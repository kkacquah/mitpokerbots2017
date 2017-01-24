# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 22:18:42 2017

@author: henoch
"""
from deuces import Card
from deuces import Evaluator
from deuces import Deck
from random import shuffle
prob = 0

def getAction(myHand,boardCards,legalActions,lastActions,history,switched):
    if switched or hasAction("DEAL",lastActions): #new cards added or hand switched
        prob = 0 #note to recheck probability of winnin
    
    
    board = []
    for card in boardCards:
        board.append(Card.new(card))
    hand = [Card.new(myHand[0]),Card.new(myHand[1])]
    
    Eval = Evaluator()
    score = Eval.evaluate(board, hand)
    #name = Eval.class_to_string(score) #if we want to know what it's called 'Straight'
    
    if prob == 0 : #check to see if probability of hand winning unknown
        prob = probabilityOfWin(hand,board,score,Eval)
    
    if hasAction("DISCARD",legalActions): #means at flop or turn and can discard card
        scores = checkMyOdds(board,hand,Eval)
        goFor = choose([score]+scores)
        
        if goFor == 0:
            return 'CHECK\n'
        else:
            return 'DISCARD:'+myHand[goFor - 1]
            
    elif not hasAction("CHECK",legalActions):  #means the person has bet #assume BET, RAISE,CALL,FOLD
        
        if prob < 30:
            if len(boardCards)>3: #on turn or river - no more chances to discard
                return 'FOLD\n' #We're not going to win
                
            else: #on flop -> one more time to discard
                scores = checkMyOdds(board,hand,Eval)
                if (score - scores[2]) < 400: #average change by switching is low
                    return 'FOLD\n'
        
        if prob > 60 :
            if prob > 80:
                return 'RAISE:#\n' # must fix with amount to raise
                
            scores = checkMyOdds(board,hand,Eval)
            if (score - scores[2]) > 200: #one more card will give even better chance
                return 'RAISE\n' 
        
        return 'CALL\n'
        
        
    else: # assume normal BET, CHECK
        if prob > 65:
            return 'BET:#\n' #fix later
        
        return 'CHECK\n'
        
def hasAction(act,actions):
    for action in actions:
        if action.find(act) != -1:
            return True
    return False
    
def checkMyOdds(board,hand,Eval):
    deck = shuffle(Deck().GetFullDeck())
    print "deck is" + deck
    
    for card in hand:
        deck.remove(card)
    for card in board:
        deck.remove(card)
    
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
    d = Deck()
    di = d.GetFullDeck() #empty list for some reason - FIX!

    deck = shuffle(di)
    print deck
    
    for card in hand:
        deck.remove(card)
    for card in board:
        deck.remove(card)
    
    possibilities = (50-len(board))*(49-len(board))
    count = 0
    
    for i in range(0,len(deck)-1):
        for j in range(i+1,len(deck)):
            testHand = [deck[i],deck[j]]
            newScore = Eval.evaluate(board, testHand)
            if score > newScore:
                count +=1
    
    return float(count)*100/possibilities
        
        
        
        
    
    
    