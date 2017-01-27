
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
stats['V_seenTurnCount'] = 0#How often player has made it to the flop
stats['V_seenTurnRate'] = 0.0
stats['V_FlopCbetCount'] = 0#How often player has bets as a raise ("ARR" stands for all reraises)
stats['V_FlopCbetRate'] = 0.0
stats['V_TurnCbetCount'] = 0#How often player makes a continuation bet after the first one ("ARRR" stands for all rereraises)
stats['V_TurnCbetRate'] = 0.0
stats['V_ftoFlopCbetCount'] = 0#How often player folds to all reraises
stats['V_ftoFlopCbetRate'] = 0.0
stats['V_ftoTurnCbetCount'] = 0#How often player folds to all rereraises
stats['V_ftoTurnCbetRate'] = 0.0
stats['V_FlopDiscardCount'] = 0#How often does the player discard at the flop
stats['V_FlopDiscardRate'] = 0.0
stats['V_TurnDiscardCount'] = 0#How often does the player discard at the turn
stats['V_TurnDiscardRate'] = 0.0
#General Statistics
stats['V_BetCount'] = 0
stats['V_CallCount'] = 0
stats['V_RaiseCount'] = 0
stats['V_FoldCount'] = 0
stats['AverageVPIPAll'] = 0.0
stats['HigherVPIPCountRate'] = 0.0
stats['HighVPIPCountRate'] = 0.0
stats['HigherVPIPCount'] = 0
stats['HighVPIPCount'] = 0
stats['TotVPIPAll'] = 0
stats['CountVPIPAll'] = 0

aggressiveEvents = ['V_pfrRate','V_vpipRate','V_3betRate','V_seenFlopRate','V_seenTurnRate','V_FlopCbetRate','V_TurnCbetRate']


def update(lastActions,myName,oppName):
	for i in range(len(lastActions)):
		lastActions[i] = lastActions[i].split(':')
	outcome = lastActions[-1]
	
	stats['numHandsPlayed']+=1
	if outcome[-1] == myName:
		stats['winCount']+=1
		stats['winAverage']= (stats['winAverage']*stats['numHandsPlayed'] + int(outcome[1]))/float(stats['numHandsPlayed'])
		stats['winRate'] = stats['winCount']/float(stats['numHandsPlayed'])
	else:
		stats['loseAverage'] = (stats['loseAverage']*stats['numHandsPlayed'] + int(outcome[1]))/float(stats['numHandsPlayed'])
	#Break up rounds into lists
	#Pre-flop raise recorder
	for round in lastActions:

		if (round[0] == 'RAISE' and round[-1] == oppName) or (round[0] == 'BET' and round[-1] == oppName):
			stats['V_pfrCount'] += 1
			stats['V_pfrRate'] = stats['V_pfrCount']/float(stats['numHandsPlayed'])
			
			break
		elif round[0] == 'DEAL':
			break

	#Init fold rate record
	for round in lastActions:
		if (round[0] == 'RAISE' and round[-1] == oppName) or (round[0] == 'CALL' and round[-1] == oppName):
			stats['V_initFoldCount'] += 1
			stats['V_initFoldRate'] = stats['V_initFoldCount']/float(stats['numHandsPlayed'])
		elif round[0] == 'DEAL':
			#If the don't call or raise during the pre-flop then they folded
			
			break
			

	#Init fold rate record	
	#VPIP recorder
	for round in lastActions:
		if (round[0] == 'RAISE' and round[-1] == oppName) or (round[0] == 'CALL' and round[-1] == oppName) or (round[0] == 'BET' and round[-1] == oppName):

			stats['V_vpipCount'] += 1
			stats['V_vpipRate'] = stats['V_vpipCount']/float(stats['numHandsPlayed'])
			break
		elif round[0] == 'DEAL':
			#If the don't call or raise during the pre-flop then they folded

			break
	#3bet raise recorder
	for round in lastActions:
		if round[0] == 'RAISE' and round[-1] == oppName:
			stats['V_pfrCount'] += 1
			stats['V_pfrRate'] = stats['V_pfrCount']/float(stats['numHandsPlayed'])

			stats['V_initFoldCount'] += 1
			stats['V_initFoldRate'] = stats['V_initFoldCount']/float(stats['numHandsPlayed'])
			break

	#3bet raise recorder

	#Fold to pfr recorder
	for i in range(len(lastActions)-1):
		if lastActions[i][0] == 'RAISE' and lastActions[i][-1] == myName and lastActions[i+1][0] == 'FOLD':
			stats['V_pfrFoldCount'] += 1
			stats['V_pfrFoldRate'] = stats['V_pfrFoldCount']/float(stats['numHandsPlayed'])
		elif round[0] == 'DEAL':
			break
	#Fold to 3bet reraise recorder
	for i in range(len(lastActions)-1):
		if lastActions[i][0] == 'RAISE' and lastActions[i][-1] == oppName and lastActions[i+1][0] == 'RAISE' and lastActions[i+2][0] == 'FOLD':
			stats['V_pfrrFoldCount'] += 1
			stats['V_pfrrFoldRate'] = stats['V_pfrrFoldCount']/float(stats['numHandsPlayed'])
		elif round[0] == 'DEAL':
			break
	for round in lastActions:
		if round[0] == 'RAISE' and round[-1] == oppName:
			stats['V_RaiseCount'] += 1
		elif round[0] == 'FOLD' and round[-1] == oppName:
			stats['V_FoldCount'] += 1
		elif round[0] == 'CALL' and round[-1] == oppName:
			stats['V_CallCount'] += 1
		elif round[0] == 'BET' and round[-1] == oppName:
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

		if lastActions[i][0] == 'DEAL' and lastActions[i][-1] == 'TURN':
			stats['V_seenTurnCount'] += 1
			stats['V_seenTurnRate'] = stats['V_seenTurnCount']/float(stats['numHandsPlayed'])
			break
	#Flop C_BET count
	for i in range(len(lastActions)-1):
		if lastActions[i] == ['DEAL','FLOP']:
			print "entered loop"
			for j in range(i,(len(lastActions))):
				print "Flop c_bet lastActions[j]: " + str(lastActions[j])
				if lastActions[j][0] == 'BET' and lastActions[j][-1] == oppName:
					stats['V_FlopCbetCount'] += 1
					stats['V_FlopCbetRate'] = stats['V_FlopCbetCount']/float(stats['numHandsPlayed'])
				if lastActions[j] == ['DEAL','TURN']:
					break           
			break
	#Turn C_BET count
	for i in range(len(lastActions)-1):
		if lastActions[i] == ['DEAL','TURN']:
			for j in range(i,(len(lastActions))):
				if lastActions[j][0] == 'BET' and lastActions[j][-1] == oppName:
					stats['V_TurnCbetCount'] += 1
					stats['V_TurnCbetRate'] = stats['V_TurnCbetCount']/float(stats['numHandsPlayed'])            
			break
	for i in range(len(lastActions)-1):
		if lastActions[i] == ['DEAL','FLOP']:
			for j in range(i,(len(lastActions))):
				if lastActions[j][0] == 'BET' and lastActions[j][-1] == myName:
					if lastActions[j+1][0] == 'FOLD' and lastActions[j+1][-1] == oppName:
						stats['V_ftoFlopCbetCount'] += 1
						stats['V_ftoFlopCbetRate'] = stats['V_ftoFlopCbetCount']/float(stats['numHandsPlayed'])            
					if lastActions[j] == ['DEAL','RIVER']:
						break     
			break
	for i in range(len(lastActions)-1):
		if lastActions[i] == ['DEAL','TURN']:
			for j in range(i,(len(lastActions))):
				if lastActions[j][0] == 'BET' and lastActions[j][-1] == myName:
					if lastActions[j+1][0] == 'FOLD' and lastActions[j+1][-1] == oppName:
						stats['V_ftoTurnCbetCount'] += 1
						stats['V_ftoTurnCbetRate'] = stats['V_ftoTurnCbetCount']/float(stats['numHandsPlayed'])            
			break
   
	for round in lastActions:
		if round[0] == 'DISCARD' and round[-1] == oppName:
			stats['V_FlopDiscardCount'] += 1
			stats['V_FlopDiscardRate'] = stats['V_FlopDiscardCount']/float(stats['numHandsPlayed'])            
			break
		elif round == ['DEAL','TURN']:
			break
	for round in lastActions:
		if round[0] == 'DISCARD' and round[-1] == oppName:
			stats['V_TurnDiscardCount'] += 1
			stats['V_TurnDiscardRate'] = stats['V_TurnDiscardCount']/float(stats['numHandsPlayed'])
		elif round == ['DEAL','RIVER']:
			break
	for round in lastActions:
		if (round[0] == 'RAISE' and round[-1] == oppName) or (round[0] == 'BET' and round[-1] == oppName):
			stats['TotVPIPAll'] += int(round[1])
			stats['CountVPIPAll'] += 1
	for round in lastActions:
		if (round[0] == 'RAISE' and round[-1] == oppName) or (round[0] == 'BET' and round[-1] == oppName):
			if (int(round[1]) >= stats['AverageVPIPAll']*1.2):
				stats['HighVPIPCount'] += 1
				stats['HighVPIPRate'] = stats['HighVPIPCount']/float(stats['numHandsPlayed'])
	for round in lastActions:
		if (round[0] == 'RAISE' and round[-1] == oppName) or (round[0] == 'BET' and round[-1] == oppName):
			if (int(round[1]) >= stats['AverageVPIPAll']*1.8):
				stats['HigherVPIPCount'] += 1
				stats['HigherVPIPRate'] = stats['HigherVPIPCount']/float(stats['numHandsPlayed'])

	try:
		stats['V_aggressionFactor'] = (stats['V_BetCount'] + stats['V_RaiseCount'])/float(stats['V_CallCount'])
	except ZeroDivisionError:
		stats['V_aggressionFactor'] = 0
	try:
		stats['V_aggressionFreq'] = (stats['V_BetCount'] + stats['V_RaiseCount'])/float(stats['V_RaiseCount'] + stats['V_FoldCount'] + stats['V_CallCount'] + stats['V_BetCount'])
	except ZeroDivisionError:
		stats['V_aggressionFactor'] = 0
	try:
		stats['AverageVPIPAll'] = stats['TotVPIPAll']/float(stats['CountVPIPAll'])
	except ZeroDivisionError:
		stats['AverageVPIPAll'] = 0	
def display_stats():
	return stats  