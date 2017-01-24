# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 22:18:42 2017

@author: henoch
"""
from deuces import Card
from deuces import Evaluator as Eval
from deuces import Deck

def getAction(myHand,boardCards,legalActions,lastActions,history):
    print hist.display_stats()
    board = []
    for card in boardCards:
        board.append(Card.new(card))
    hand = [Card.new(myHand[0]),Card.new(myHand[1])]
    
    score = Eval.evaluate(board, hand)
    name = Eval.class_to_string(score)
    
    if hasAction("DISCARD",legalActions):
        goForIt = checkMyOdds(board,hand)
        if goForIt = 0:
            return 'CHECK\n'
        else:
            return 'DISCARD:'+myHand[goForIt - 1]
        
        
def hasAction(act,actions):
    for action in actions:
        if action.find(act) != -1:
            return True
    return False
    
def checkMyOdds(board,hand,currentScore):
    deck = Deck().GetFullDeck().shuffle()
    for card in hand:
        deck.remove(card)
    for card in board:
        deck.remove(card)
    
    firstAverage = getAverage(0,deck[:],hand,board)
    secondAverage = getAverage(1,deck[:],hand,board)
    
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

def getAverage(index,deck,hand,board):
    total = 0
    count = 0
    while deck.len() > 0:
        newCard = deck.pop(0)
        testHand = hand[:]
        testHand[index] = newCard
        newScore = Eval.evaluate(board, testHand)
        total += newScore
        count += 1
    
    return total / float(count)
        
        
        
        
    
    
    