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

def getAction(myHand,boardCards,legalActions,lastActions,history,switched,button):

    board = []
    for card in boardCards:
        board.append(Card.new(card))
    hand = [Card.new(myHand[0]),Card.new(myHand[1])]

    deck = data.get('deck',[])
    if len(deck) <= 1:
        fillDeck(board,hand)
    
    if len(board) == 0:
        return preflop(myHand,legalActions,lastActions,history,button)

    if switched or hasAction("DEAL",lastActions) != -1 or data.get('score',0.0) == 0.0 or data.get('prob',0.0) == 0.0: #new cards added or hand switched
        if switched:
            print 'card was switched'
            updateDeck(hand,board)
            
        print 'calculating score and prob'
        Eval = Evaluator()
        data['score'] = Eval.evaluate(hand,board)  
        probabilityOfWin(hand,board,Eval)
    else:
        print 'score and probability already calculated'
    
    score = data.get('score',10000)
    print 'score det as ' + str(score)
    probWin = data.get('prob',0.0)
    print 'naive prob det as ' + str(probWin)
    
    prob = probWin * CalculateStrength(PastAggressiveEvents(lastActions),history) 
         
    if hasAction("DISCARD",legalActions) != -1: #means at flop or turn and can discard card
        scores = checkMyOdds(hand,board)
        print 'I have discard option my score is ' + str(score)
        print 'Averages are ' + str(scores)
        goFor = choose([score]+scores)
        print 'so I choose ' + str(goFor)
        
        if goFor == 0:
            return 'CHECK\n'
        else:
            return 'DISCARD:'+myHand[goFor - 1]+'\n'

    elif hasAction("CHECK",legalActions) == -1:  #means the person has bet -> cannot CHECK #assume RAISE,CALL,FOLD
        print 'cp 1'

        if prob < 30:
            print 'cp 2'
            if len(boardCards)>3: #on turn or river - no more chances to discard
                return 'FOLD\n' #We're not going to win

            else: #on flop -> one more time to discard
                print 'cp 4'
                scores = checkMyOdds(hand,board)
                print 'average score can be' + str(scores)
                if (scores[0] - score) > -700 and (scores[1] - score) > -700: #average change by switching is low
                    return 'FOLD\n'
                    
        canRaise = hasAction("RAISE",legalActions)

        if prob > 60 and canRaise != -1:
            print 'cp 3'            
            raises = legalActions[canRaise].split(':')
            print 'raises: ' + str(raises)
            
            if prob > 80:
                print 'My odds GREAT'
                raiseTo = (int(raises[1])+2*int(raises[2]))/3 #close to max
                return 'RAISE:'+str(raiseTo)+'\n'

            scores = checkMyOdds(hand,board)
            print 'cp 5'
            print 'average score can be' + str(scores)
            if (scores[1] - score) < 0 or (scores[0] - score) < 0: #have odds to increase more
                raiseTo = (int(raises[1])+int(raises[2]))/2
                return 'RAISE:'+str(raiseTo)+'\n'

        return 'CALL\n'


    else: # assume normal BET, CHECK, FOLD
        print 'cp 6'
        canBet = hasAction("BET",legalActions)
        if prob > 65 and canBet != -1:
            print 'cp 7'
            bets = legalActions[canBet].split(':')
            print 'bets: ' + str(bets)
            
            bet = (2*int(bets[1])+int(bets[2]))/3
            return 'BET:'+ str(bet) + '\n' 

        return 'CHECK\n'
        
def preflop(myHand,legalActions,lastActions,history,button):
    haveGoodCards = goodCards(myHand)
    print 'I rate my cards: ' + str(haveGoodCards) + '/10' 
    
    if hasAction("POST",lastActions) != -1: #no bets yet
        if button == 'true' or button == 'True': #we go first
            print 'button is true'
            if haveGoodCards >= 5: #only with good cards
                canRaise = hasAction("RAISE",legalActions)
                raises = legalActions[canRaise].split(':')
                raiseTo = ((15-haveGoodCards)*int(raises[1])+int(raises[2]))/(16-haveGoodCards) #increases as cards are better
                return 'RAISE:'+ str(raiseTo) + '\n' 
            return 'CALL\n'
            
        else: #button = false, other player went first, We go first after flop
            print 'button is false'
            if hasAction("CHECK",legalActions) == -1: #villain raised
                if haveGoodCards <= 1: #our cards are terrible
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
        if button == 'true' or button == 'True': #person bet after we called/raised
            print 'button is true2'
            if haveGoodCards <= 1:
                return 'FOLD\n'
                
            return 'CALL\n'
        else: #person reraised our raise (since we went second) 
            print 'button is false2'
            if haveGoodCards <= 1:
                return 'FOLD\n'
            return 'CALL\n'
            
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
    print "list of actions are: " + str(actions)
    for i in range(0,len(actions)):
        if actions[i].find(act) != -1:
            print "has wanted act: " + str(act)
            return i
    print "doesn't have wanted act: " + str(act)
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
        