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
data['prob'] = 0.0 #here so it is not always recalculated
data['deck'] = [] #deck saved here so discarded card stays removed
data['score'] = 0

def getAction(myHand,boardCards,legalActions,FullLastActions,lastActions,history,switched,button,oppName,potSize):

    board = []
    for card in boardCards:
        board.append(Card.new(card))
    hand = [Card.new(myHand[0]),Card.new(myHand[1])]

    deck = data.get('deck',[])
    if len(deck) <= 1:
        fillDeck(board,hand)
    
    if len(board) == 0:
        return preflop(myHand,legalActions,lastActions,history,button,potSize,FullLastActions)

    if switched or hasAction("DEAL",lastActions) != -1 or data.get('score',0.0) == 0.0 or data.get('prob',0.0) == 0.0: #new cards added or hand switched
        if switched:
            updateDeck(hand,board)
        Eval = Evaluator()
        data['score'] = Eval.evaluate(hand,board)  
        probWin = probabilityOfWin(hand,board,Eval)
        if history['numHandsPlayed'] >= 100:
            print "probwin: " + str(probWin)
            if probWin <= 85:
                prob = probWin * CalculateStrength(PastAggressiveEvents(FullLastActions,oppName,history),history)
                print "prob: " + str(prob)
            else:
                prob = probWin
        else:
            prob = probWin
        data['prob'] = prob

    score = data.get('score',10000)
    prob = data.get('prob',0.0)
    
    if hasAction("DISCARD",legalActions) != -1: #means at flop or turn and can discard card
        scores = checkMyOdds(hand,board)
        goFor = choose([score]+scores)
        
        if goFor == 0:
            return 'CHECK\n'
        else:
            return 'DISCARD:'+myHand[goFor - 1]+'\n'

    elif hasAction("CHECK",legalActions) == -1:  #means the person has bet -> cannot CHECK #assume RAISE,CALL,FOLD
        RaiseIndex = hasAction("RAISE",lastActions)
        BetIndex = hasAction("BET",lastActions)
        PIPindex = max(RaiseIndex,BetIndex)
        
        index = hasAction("BET",lastActions)
        changeInBet = 0
        lastBet = potSize
        if (index == -1):
            RaiseIndex = hasAction("RAISE",lastActions)
            last = lastRaises(FullLastActions[:])
            print 'last: ' +str(last)
            lastBet = last[0]
            changeInBet = last[1] - lastBet
        else:
            betAction = (lastActions[index])[:].split(':')
            #print 'betaction:' + str(betAction)
            changeInBet = int(betAction[1])
        print 'change in bet size: ' + str(changeInBet)
        
        if prob < 50:
            print "LEts fold!!!!"
            if len(boardCards)>3: #on turn or river - no more chances to discard
                return 'FOLD\n' #We're not going to win

            else: #on flop -> one more time to discard
                scores = checkMyOdds(hand,board)
                if (scores[0] - score) > -1000 and (scores[1] - score) > -1000: #average change by switching is low
                    return 'FOLD\n'
        
        if prob < 60 and changeInBet > 60:
            return 'FOLD\n'
        if prob < 70 and changeInBet > 100:
            return 'FOLD\n'
        elif prob < 75 and changeInBet > 150:
            return 'FOLD\n'
                    
        canRaise = hasAction("RAISE",legalActions)

        if prob > 70 and canRaise != -1:       
            raises = legalActions[canRaise].split(':')
            
            if prob >= 80:
                raiseTo = (int(raises[1])*(1 + (prob/2/100))*(1 + (prob/2/100))/1.5) #close to max
                return 'RAISE:'+str(min(int(raises[2]),raiseTo))+'\n'

            scores = checkMyOdds(hand,board)
            if (scores[1] - score) > 400 and (scores[0] - score) > 400: #not much better than this
                raiseTo = (int(raises[1]))
                return 'RAISE:'+str(min(int(raises[2]),raiseTo))+'\n'
        
        return 'CALL\n'


    else: # assume normal BET, CHECK, FOLD
        canBet = hasAction("BET",legalActions)
        if prob > 65 and canBet != -1:
            bets = legalActions[canBet].split(':')
            
            bet = ((1+(prob/2/100))*(1+(prob/2/100))*int(bets[1])+0.15*int(bets[2]))/2
            return 'BET:'+ str(min(int(bets[2]),bet)) + '\n' 

        return 'CHECK\n'
        
def preflop(myHand,legalActions,lastActions,history,button,potSize,FullLastActions):
    haveGoodCards = goodCards(myHand)
    
    index = hasAction("POST",lastActions)
    changeInBet = 0
    lastBet = potSize
    if (index == -1):
        RaiseIndex = hasAction("RAISE",lastActions)
        last = lastRaises(FullLastActions[:])
        lastBet = last[0]
        changeInBet = last[1] - lastBet
    else:
        #betAction = lastActions[index][:].split(':')
        changeInBet = 2

    if index != -1: #no bets yet
        if button == 'true' or button == 'True': #we go first
            if haveGoodCards >= 5: #only with good cards
                canRaise = hasAction("RAISE",legalActions)
                raises = legalActions[canRaise].split(':')
                raiseTo = ((15-haveGoodCards)*int(raises[1])+int(raises[2]))/(16-haveGoodCards) #increases as cards are better
                return 'RAISE:'+ str(raiseTo) + '\n' 
            return 'CALL\n'
            
        else: #button = false, other player went first, We go first after flop

            if hasAction("CHECK",legalActions) == -1: #villain raised
                if haveGoodCards <= 2: #our cards are terrible
                    return 'FOLD\n'
                elif changeInBet > 30 and haveGoodCards < 4:
                    return 'FOLD\n'
                elif changeInBet > 70 and haveGoodCards <= 6:
                    return 'FOLD\n'
                elif changeInBet > 150 and haveGoodCards < 8:
                    return 'FOLD\n'
                    
                return 'CALL\n'
                
            else: #villain called
                if haveGoodCards >= 4:
                    canRaise = hasAction("RAISE",legalActions)
                    raises = legalActions[canRaise].split(':')
                    raiseTo = ((13-haveGoodCards)*int(raises[1])+int(raises[2]))/(14-haveGoodCards) #increases as cards are better
                    return 'RAISE:'+ str(raiseTo) + '\n' 
                    
                return 'CHECK\n'
                
    else: #some action happened after post
        if haveGoodCards <= 2: #our cards are terrible
            return 'FOLD\n'
        elif changeInBet > 30 and haveGoodCards <= 4:
            return 'FOLD\n'
        elif changeInBet > 70 and haveGoodCards <= 6:
            return 'FOLD\n'
        elif changeInBet > 150 and haveGoodCards < 8:
            return 'FOLD\n'
                    
        return 'CALL\n'
        """if button == 'true' or button == 'True': #person bet after we called/raised
            
            if haveGoodCards <= 1:
                return 'FOLD\n'
                
            return 'CALL\n'
        else: #person reraised our raise (since we went second) 
            if haveGoodCards <= 1:
                return 'FOLD\n'
            return 'CALL\n' """
            
def goodCards(myHand): #returns integer based on relative value of original cards
    cards = ['0','1','2','3','4','5','6','7','8','9','T','J','Q','K','A']
    firstNum = cards.index(myHand[0][0])
    firstSuit = myHand[0][1]
    secondNum = cards.index(myHand[1][0])   
    secondSuit = myHand[1][1]
    
    if firstNum == secondNum:
        if firstNum>=9:
            return 8 # high pair
        return 3 # pair
    elif abs(firstNum - secondNum) < 5: #within a  straight away
        if firstSuit == secondSuit:
            if min(firstNum,secondNum)>=9:
                return 9 # ~ royal flush
            return 6 # ~ straight flush
            
        if min(firstNum,secondNum)>=9:
            return 4 # ~ high straight
        elif max(firstNum,secondNum)>=10:
            return 2 #high card
            
        return 1 # ~ straight - rarely means anything especially when we are going to switch cards
    elif firstSuit == secondSuit:
        if max(firstNum,secondNum)>=11:
            return 7 # ~ high flush
        return 5 # ~ flush
    elif max(firstNum,secondNum)>=10:
        return 2 #high card
      
    return 0 #useless cards (i.e. 2h 7s)
    
def hasAction(act,actions): #returns index of action in list without ValueError
    
    for i in range(0,len(actions)):
        if actions[i].find(act) != -1:
            return i
    
    return -1

def checkMyOdds(hand,board):
    deck = list(data.get("deck",fillDeck(hand,board)))
    shuffle(deck)
    Eval = Evaluator()

    firstAverage = getAverage(0,deck[:],hand,board,Eval)
    secondAverage = getAverage(1,deck[:],hand,board,Eval)

    return [firstAverage,secondAverage]
    
def choose(scores):
    currentScore = scores[0]
    firstAverage = scores[1]
    secondAverage = scores[2]
    
    smallScore = min(currentScore,firstAverage,secondAverage)
    if smallScore == currentScore:
        return 0
    elif smallScore == firstAverage:
        return 1
    else:
        return 2
    
def getAverage(index,deck,hand,board,Eval):
    total = 0
    count = 0
    while len(deck) > 0:
        newCard = deck.pop(0)
        testHand = hand[:]
        testHand[index] = newCard
        newScore = Eval.evaluate(testHand,board)
        total += newScore
        count += 1

    return total / float(count)

def probabilityOfWin(hand,board,Eval):
    deck = data.get("deck",fillDeck(board,hand)) #get already made deck or new
    shuffle(deck)
    
    myScore = data.get('score',9000)
    
    possibilities = len(deck)*(len(deck)-1)
    count = 0

    for i in range(0,len(deck)-1):
        for j in range(i+1,len(deck)):
            testHand = [deck[i],deck[j]]
            newScore = Eval.evaluate(testHand,board)
            if myScore <= newScore:
                count +=2 #our hand would win against random hand

    prob = float(count)*100/possibilities
    data['prob'] = prob
    return prob

def fillDeck(hand,board):
    d = Deck()
    deck = d.GetFullDeck()
    shuffle(deck)


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
            
    for card in board:
        if card in deck: #make sure card hasn't been removed
            deck.remove(card)
    
    data['deck'] = deck
    return deck

def PastAggressiveEvents(lastActions,oppName,stats):

    aggressiveEventsOccurred = []
    for i in range(len(lastActions)):
        lastActions[i] = lastActions[i].split(':')
    for round in lastActions:
        if (round[0] == 'RAISE' and round[-1] == oppName) or (round[0] == 'BET' and round[-1] == oppName):
            aggressiveEventsOccurred.append('V_pfrRate')
            break
        elif round[0] == 'DEAL':
            break
    for round in lastActions:
        if (round[0] == 'RAISE' and round[-1] == oppName) or (round[0] == 'CALL' and round[-1] == oppName) or (round[0] == 'BET' and round[-1] == oppName):
            aggressiveEventsOccurred.append('V_vpipRate')
            break
        elif round[0] == 'DEAL':
            break
    for round in lastActions:
        if round[0] == 'BET' and round[-1] == oppName:
            aggressiveEventsOccurred.append('V_3betRate')
            break
        elif round[0] == 'DEAL':
            break
    for i in range(len(lastActions)-1):
        if lastActions[i][0] == 'DEAL' and lastActions[i][-1] == 'FLOP':
             aggressiveEventsOccurred.append('V_seenFlopRate')
             break
    for i in range(len(lastActions)-1):
         if lastActions[i][0] == 'DEAL' and lastActions[i][-1] == 'FLOP':
             aggressiveEventsOccurred.append('V_seenTurnRate')
             break
    for i in range(len(lastActions)-1):
        if round == ['DEAL','FLOP']:
            for j in range(i,(len(lastActions))):
                if lastActions[j][0] == 'BET' and lastActions[j][-1] == oppName:
                    aggressiveEventsOccurred.append('V_FlopCbetRate')           
            break
    for i in range(len(lastActions)-1):
        if round == ['DEAL','TURN']:
            for j in range(i,(len(lastActions))):
                if lastActions[j][0] == 'BET' and lastActions[j][-1] == oppName:
                    aggressiveEventsOccurred.append('V_TurnCbetRate')            
            break
    for round in lastActions:
        if (round[0] == 'RAISE' and round[-1] == oppName):
            if (int(round[1]) >= stats['StdDevRaiseAll']):
                aggressiveEventsOccurred.append('HighRaiseRate')
    for round in lastActions:
        if (round[0] == 'RAISE' and round[-1] == oppName):
            if (int(round[1]) >= stats['StdDevRaiseAll']*1.5):
                aggressiveEventsOccurred.append('HigherRaiseRate')
    for round in lastActions:
        if (round[0] == 'BET' and round[-1] == oppName):
            if (int(round[1]) >= stats['StdDevBetAll']):
                aggressiveEventsOccurred.append('HighBetRate')
    for round in lastActions:
        if (round[0] == 'BET' and round[-1] == oppName):
            if (int(round[1]) >= stats['StdDevBetAll']*1.5):
                aggressiveEventsOccurred.append('HigherBetRate')
    

    return aggressiveEventsOccurred
    
def CalculateStrength(aggressiveEventsOccurred, stats):
    aggressiveEvents = ['V_pfrRate','V_vpipRate','V_seenTurnRate','V_FlopCbetRate','V_TurnCbetRate','HighRaiseRate','HigherRaiseRate','HighBetRate','HigherBetRate']
    
    strengthDenominator = 0
    print "aggression Freq is: " + str(stats['V_aggressionFreq'])
    strength = 1+stats['V_aggressionFreq']
    for event in aggressiveEvents:
        print stats[event]
        try:
            strengthDenominator += 1/float(stats[event])

        except ZeroDivisionError:
            strengthDenominator += 0

    for event in aggressiveEventsOccurred:
            print "this event occured: " + event + ", here is its stat: " + str(stats[event])
            try:        
                strength -= ((1/float(stats[event]))/float(strengthDenominator))
            except ZeroDivisionError:
                strength += 0
    return strength
    
def lastRaises(FullLastActions):
    newRaise = 0
    oldRaise = 0
    for i in range(len(FullLastActions)-1,0,-1):
        action = FullLastActions[i]
        if  action.find("RAISE") != -1 or action.find("BET") != -1 or  action.find("POST") != -1:
                if newRaise == 0:
                    newRaise = int(action.split(':')[1])
                    continue
                oldRaise = int(action.split(':')[1])
                break
    
    return (oldRaise,newRaise)



