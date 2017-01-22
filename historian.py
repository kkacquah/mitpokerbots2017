#Historian Class
#Global Variables
stats = dict()
stats['numHandsPlayed']= 0 #Hands Played so far
stats['winCount'] = 0 #Your win count
stats['winRate'] = 0 #Your win rate
stats['winAverage'] = 0 #Your win rate
stats['loseAverage'] = 0 #Your win rate
#Your win rate
#Pre-Flop Statistics

#A prefix of V_ denotes the villain, a prefix of H_ denotes the hero
stats['V_pfrCount']= 0#pre-flop raise
stats['V_pfrRate']= 0.0
stats['V_vpipCount'] = 0#call or raise pre-flop
stats['V_vpipRate'] = 0.0
stats['V_initFoldCount'] = 0#related to vpip, counts when they don't play their hand
stats['V_initFoldRate'] = 0.0
stats['V_ThreeBCount'] = 0#How many times the opponent 3-bet
stats['V_ThreeBRate'] = 0.0
stats['V_pfrFoldCount'] = 0#Fold to initial pre-flop raise
stats['V_pfrFoldRate'] = 0.0
stats['V_pfrrFoldCount'] = 0#Fold to Pre-flop Re-raise
stats['V_pfrrFoldRate'] = 0.0
#Post-Flop Statistics

stats['V_aggressionFactor']= 0.0#(Bet + Raise) / Call
stats['V_aggressionFreq']= 0.0#(total bet + total raise) / (total bet + total raise + total call + total fold) * 100
stats['V_wtsdCount'] = 0#How often player goes to showdown after seeing flop (can be used with aggression)
stats['V_wtsdRate'] = 0.0
stats['V_showdownCount'] = 0#How often player goes to showdown in total
stats['V_showdownRate'] = 0.0
stats['V_seenFlopCount'] = 0#How often player has made it to the flop
stats['V_seenFlopRate'] = 0.0
stats['V_arrCount'] = 0#How often player has bets as a raise ("ARR" stands for all reraises)
stats['V_arrRate'] = 0.0
stats['V_arrrCount'] = 0#How often player makes a continuation bet after the first one ("ARRR" stands for all rereraises)
stats['V_arrrRate'] = 0.0
stats['V_ftoarrCount'] = 0#How often player folds to all reraises
stats['V_ftoarrRate'] = 0.0
stats['V_ftoarrrCount'] = 0#How often player folds to all rereraises
stats['V_ftoarrrRate'] = 0.0
stats['V_FlopDiscardCount'] = 0#How often does the player discard at the flop
stats['V_FlopDiscardRate'] = 0.0
stats['V_TurnDiscardCount'] = 0#How often does the player discard at the turn
stats['V_TurnDiscardRate'] = 0.0
#General Statistics
stats['V_BetCount'] = 0
stats['V_CallCount'] = 0
stats['V_RaiseCount'] = 0
stats['V_FoldCount'] = 0

def update(lastActions):
    for i in range(len(lastActions)):
        lastActions[i] = lastActions[i].split(':')
    outcome = lastActions[-1]
    
    stats['numHandsPlayed']+=1
    if outcome[-1] == 'player1':
        stats['winCount']+=1
        stats['winAverage']= (stats['winAverage']*stats['numHandsPlayed'] + int(outcome[1]))/float(stats['numHandsPlayed'])
        stats['winRate'] = stats['winCount']/float(stats['numHandsPlayed'])
    else:
        stats['loseAverage'] = (stats['loseAverage']*stats['numHandsPlayed'] + int(outcome[1]))/float(stats['numHandsPlayed'])
    #Break up rounds into lists
    #Pre-flop raise recorder
    for round in lastActions:
        if round[0] == 'RAISE' and round[-1] == 'player2':
            stats['V_pfrCount'] += 1
            stats['V_pfrRate'] = stats['V_pfrCount']/float(stats['numHandsPlayed'])
            
            break
        elif round[0] == 'DEAL':
            break
    #Init fold rate record
    for round in lastActions:
        if (round[0] == 'RAISE' and round[-1] == 'player2') or (round[0] == 'CALL' and round[-1] == 'player2'):
            stats['V_initFoldCount'] += 1
            stats['V_initFoldRate'] = stats['V_initFoldCount']/float(stats['numHandsPlayed'])
        elif round[0] == 'DEAL':
            #If the don't call or raise during the pre-flop then they folded
            
            break
            
    #VPIP recorder
    for round in lastActions:
        if (round[0] == 'RAISE' and round[-1] == 'player2') or (round[0] == 'CALL' and round[-1] == 'player2'):
            stats['V_vpipCount'] += 1
            stats['V_vpipRate'] = stats['V_vpipCount']/float(stats['numHandsPlayed'])
            break
            break
        elif round[0] == 'DEAL':
            #If the don't call or raise during the pre-flop then they folded
            
            break
    #3bet raise recorder
    for round in lastActions:
        if round[0] == 'RAISE' and round[-1] == 'player2':
            stats['V_pfrCount'] += 1
            stats['V_pfrRate'] = stats['V_pfrCount']/float(stats['numHandsPlayed'])
            break
        elif round[0] == 'DEAL':
            break
    #3bet raise recorder
    for round in lastActions:
        if round[0] == 'RAISE' and round[-1] == 'player2':
            stats['V_ThreeBCount'] += 1
            stats['V_ThreeBRate'] = stats['V_ThreeBCount']/float(stats['numHandsPlayed'])
            break
        elif round[0] == 'DEAL':
            break
    #Fold to 3bet raise recorder
    for i in range(len(lastActions)-1):
        if lastActions[i][0] == 'RAISE' and lastActions[i][-1] == 'player1' and lastActions[i+1][0] == 'FOLD':
            stats['V_pfrFoldCount'] += 1
            stats['V_pfrFoldRate'] = stats['V_pfrFoldCount']/float(stats['numHandsPlayed'])
        elif round[0] == 'DEAL':
            break
    #Fold to 3bet reraise recorder
    for i in range(len(lastActions)-1):
        if lastActions[i][0] == 'RAISE' and lastActions[i][-1] == 'player2' and lastActions[i+1][0] == 'RAISE' and lastActions[i+2][0] == 'FOLD':
            stats['V_pfrrFoldCount'] += 1
            stats['V_pfrrFoldRate'] = stats['V_pfrrFoldCount']/float(stats['numHandsPlayed'])
        elif round[0] == 'DEAL':
            break
    for round in lastActions:
        if round[0] == 'RAISE' and round[-1] == 'player2':
            stats['V_RaiseCount'] += 1
        elif round[0] == 'FOLD' and round[-1] == 'player2':
            stats['V_FoldCount'] += 1
        elif round[0] == 'CALL' and round[-1] == 'player2':
            stats['V_CallCount'] += 1
        elif round[0] == 'BET' and round[-1] == 'player2':
            stats['V_BetCount'] += 1
    for i in range(len(lastActions)-1):
        if lastActions[i][0] == 'DEAL' and lastActions[i][-1] == 'FLOP':
            for j in range(i,(len(lastActions))):
                if lastActions[j][0] == 'SHOW':
                    stats['V_wtsdCount'] += 1
                    stats['V_wtsdRate'] = stats['V_wtsdCount']/float(stats['numHandsPlayed'])
    for i in range(len(lastActions)-1):
             if lastActions[i][0] == 'SHOW':
                    stats['V_showdownCount'] += 1
                    stats['V_showdownRate'] = stats['V_showdownCount']/float(stats['numHandsPlayed'])
    for i in range(len(lastActions)-1):
        if lastActions[i][0] == 'DEAL' and lastActions[i][-1] == 'FLOP':
            stats['V_seenFlopCount'] += 1
            stats['V_seenFlopRate'] = stats['V_seenFlopCount']/float(stats['numHandsPlayed'])
            break
    for i in range(len(lastActions)-1):
        if lastActions[i][0] == 'RAISE' and lastActions[i][-1] == 'player1':
            print "entered first loop"
            for j in range(i,(len(lastActions))):
                print lastActions[j]
                if lastActions[j][0] == 'RAISE' and lastActions[j][-1] == 'player2':
                    stats['V_arrCount'] += 1
                    stats['V_arrRate'] = stats['V_arrCount']/float(stats['numHandsPlayed'])            
            break
    for i in range(len(lastActions)-1):
        if lastActions[i][0] == 'RAISE' and lastActions[i][-1] == 'player2':
            for j in range(i,(len(lastActions))):
                if lastActions[j][0] == 'RAISE' and lastActions[j][-1] == 'player1':
                    for k in range(j,(len(lastActions))):
                        if lastActions[k][0] == 'RAISE' and lastActions[k][-1] == 'player2':
                            stats['V_arrrCount'] += 1
                            stats['V_arrrRate'] = stats['V_arrCount']/float(stats['numHandsPlayed'])            
            break
    #fotarr counter        
    for i in range(len(lastActions)-1):
        if lastActions[i][0] == 'RAISE' and lastActions[i][-1] == 'player2':
            for j in range(i,(len(lastActions))):
                if lastActions[j][0] == 'RAISE' and lastActions[j][-1] == 'player1':
                    for k in range(j,(len(lastActions))):
                        if lastActions[k][0] == 'FOLD' and lastActions[k][-1] == 'player2':
                            stats['V_ftoarrCount'] += 1
                            stats['V_ftoarrRate'] = stats['V_ftoarrCount']/float(stats['numHandsPlayed'])            
            break
    for i in range(len(lastActions)-1):
        if lastActions[i][0] == 'RAISE' and lastActions[i][-1] == 'player1':
            for j in range(i,(len(lastActions))):
                if lastActions[j][0] == 'RAISE' and lastActions[j][-1] == 'player2':
                    for k in range(j,(len(lastActions))):
                        if lastActions[k][0] == 'RAISE' and lastActions[k][-1] == 'player1':
                            for l in range(l,(len(lastActions))):
                                if lastActions[l][0] == 'FOLD' and lastActions[l][-1] == 'player2':
                                    stats['V_ftoarrrCount'] += 1
                                    stats['V_ftoarrrRate'] = stats['V_ftoarrrCount']/float(stats['numHandsPlayed'])            
            break
    for round in lastActions:
        if round[0] == 'DISCARD' and round[-1] == 'player2':
            stats['V_FlopDiscardCount'] += 1
            stats['V_FlopDiscardRate'] = stats['V_FlopDiscardCount']/float(stats['numHandsPlayed'])            
            break
        elif round == ['DEAL','TURN']:
            break
    for round in lastActions:
        if round[0] == 'DISCARD' and round[-1] == 'player2':
            stats['V_TurnDiscardCount'] += 1
            stats['V_TurnDiscardRate'] = stats['V_TurnDiscardCount']/float(stats['numHandsPlayed'])
            
            break
        elif round == ['DEAL','RIVER']:
            break
    try:
        stats['V_aggressionFactor'] = (stats['V_BetCount'] + stats['V_RaiseCount'])/float(stats['V_CallCount'])
    except ZeroDivisionError:
        stats['V_aggressionFactor'] = 0
    try:
        stats['V_aggressionFreq'] = (stats['V_BetCount'] + stats['V_RaiseCount'])/float(stats['V_RaiseCount'] + stats['V_FoldCount'] + stats['V_CallCount'] + stats['V_BetCount'])*100
    except ZeroDivisionError:
        stats['V_aggressionFactor'] = 0
def display_stats():
    return stats  