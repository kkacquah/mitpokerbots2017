# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 22:18:42 2017

@author: henoch
"""
from deuces import Card
from deuces import Evaluator
from deuces import Deck
from random import shuffle
probWin = 0
def getAction(myHand,boardCards,legalActions,lastActions,recentLastActions,history,switched,newhand):
    print lastActions
    if switched or ('DEAL:FLOP' in recentLastActions) or ('DEAL:TURN' in recentLastActions) or newhand: #new cards added or card discarded
        probWin = 0 #note to recheck probability of winning

    
    
    board = []
    for card in boardCards:
        board.append(Card.new(card))
    hand = [Card.new(myHand[0]),Card.new(myHand[1])]
    
    Eval = Evaluator()
    score = Eval.evaluate(board, hand)
    #name = Eval.class_to_string(score) #if we want to know what it's called 'Straight'
    #prob is the probability of winning multiplied by the chance that we have a stronger hand than our opponent
    #The probability that we have a stronger hand than our opponent is calculated by "Hand Strength"
    
    if probWin == 0 : #check to see if probability of hand winning unknown
        probWin = probabilityOfWin(hand,board,score,Eval)
    prob = probWin*CalculateStrength(PastAggressiveEvents(lastActions),history)
    if hasAction("DISCARD",legalActions): #means at flop or turn and can discard card
        scores = checkMyOdds(board,hand,Eval)
        goFor = choose([score]+scores)
        
        if goFor == 0:
            return 'CHECK\n'
        else:
            return 'DISCARD:'+ myHand[goFor - 1] + '\n'
            
    elif not hasAction("CHECK",legalActions):  #means the person has bet #assume BET, RAISE,CALL,FOLD
        
        if prob < 30:
            if len(boardCards)>3: #on turn or river - no more chances to discard
                return 'FOLD\n' #We're not going to win
                
            else: #on flop -> one more time to discard
                scores = checkMyOdds(board,hand,Eval)
                if (score - max(scores)) < 400: #maximum change by switching is low
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
    deck = Deck().GetFullDeck()
    
    for card in hand:
        deck.remove(card)
    for card in board:
        deck.remove(card)
    
    firstAverage = getAverage(0,deck[:],hand,board,Eval)
    secondAverage = getAverage(1,deck[:],hand,board,Eval)

    return [firstAverage,secondAverage]
def choose(scores):
    currentScore = scores[0]
    firstAverage = scores[1]
    secondAverage = scores[2]
    
    max = max(currentScore,firstAverage,secondAverage)
    if max == currentScore:
        return 0
    elif max == firstAverage:
        return 1
    elif max == secondAverage:
        return 2
    
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
    deck = d.GetFullDeck() #empty list for some reason - FIX!
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
    print float(count)*100/possibilities
    return float(count)*100/possibilities
def PastAggressiveEvents(lastActions):
    aggressiveEventsOccurred = []
    for round in lastActions:
        if (round[0] == 'RAISE' and round[-1] == 'player2') or (round[0] == 'BET' and round[-1] == 'player2'):
            aggressiveEvents.append('V_pfrCount')
            break
        elif round[0] == 'DEAL':
            break
    for round in lastActions:
        if (round[0] == 'RAISE' and round[-1] == 'player2') or (round[0] == 'CALL' and round[-1] == 'player2') or (round[0] == 'BET' and round[-1] == 'player2'):
            aggressiveEvents.append('V_vpipCount')
            break
        elif round[0] == 'DEAL':
            break
    for round in lastActions:
        if round[0] == 'BET' and round[-1] == 'player2':
            aggressiveEvents.append('V_3betCount')
            break
        elif round[0] == 'DEAL':
            break
    for i in range(len(lastActions)-1):
        if lastActions[i][0] == 'DEAL' and lastActions[i][-1] == 'FLOP':
            aggressiveEvents.append('V_seenFlopCount')
            break
    for i in range(len(lastActions)-1):
        if lastActions[i][0] == 'DEAL' and lastActions[i][-1] == 'FLOP':
            aggressiveEvents.append('V_seenTurnCount')
            break
    for i in range(len(lastActions)-1):
        if round == ['DEAL','FLOP']:
            for j in range(i,(len(lastActions))):
                print lastActions[j]
                if lastActions[j][0] == 'BET' and lastActions[j][-1] == 'player2':
                    aggressiveEvents.append('V_FlopCbetCount')           
            break
    for i in range(len(lastActions)-1):
        if round == ['DEAL','TURN']:
            for j in range(i,(len(lastActions))):
                print lastActions[j]
                if lastActions[j][0] == 'BET' and lastActions[j][-1] == 'player2':
                    aggressiveEvents.append('V_TurnCbetCount')            
            break

    return aggressiveEventsOccurred
def CalculateStrength(aggressiveEventsOccurred, stats):
    aggressiveEvents = ['V_pfrRate','V_vpipRate','V_3betRate','V_seenFlopRate','V_seenTurnRate','V_FlopCbetRate','V_TurnCbetRate']
    strengthDenominator = 0
    for event in aggressiveEvents:
        strengthDenominator += stats[event]
    strength = 1
    for event in aggressiveEventsOccurred:
        strength -= stats[event]/float(strengthDenominator)
    return strength
        
        
        
    
    
    