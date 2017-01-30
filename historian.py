import math
#Historian Class
#Global Variables
stats = dict()
stats['numHandsPlayed']= 0 #Hands Played so far
stats['winCount'] = 0 #Your win count
stats['winRate'] = 0 #Your win rate
stats['winAverage'] = [] #Your win rate
stats['V_winAverageWA']= 0.0
stats['loseAverage'] = [] #Your win rate
stats['V_loseAverageWA']= 0.0
#Your win rate
#Pre-Flop Statistics

#A prefix of V_ denotes the villain, a prefix of H_ denotes the hero
stats['V_pfrCount']= 0#pre-flop raise
stats['V_pfrRate']= []
stats['V_pfrRateWA']= 0.0

stats['V_vpipCount'] = 0#call or raise pre-flop
stats['V_vpipRate'] = []
stats['V_vpipRateWA']= 0.0

stats['V_initFoldCount'] = 0#related to vpip, counts when they don't play their hand
stats['V_initFoldRate'] = []
stats['V_initFoldRateWA']= 0.0

stats['V_pfrFoldCount'] = 0#Fold to initial pre-flop raise
stats['V_pfrFoldRate'] = []
stats['V_pfrFoldRateWA']= 0.0

stats['V_pfrrFoldCount'] =0#Fold to Pre-flop Re-raise
stats['V_pfrrFoldRate'] = []
stats['V_pfrrFoldRateWA']= 0.0

#Post-Flop Statistics

stats['V_aggressionFactor']= []#(Bet + Raise) / Call
stats['V_aggressionFactorWA']= 0.0

stats['V_aggressionFreq']= []#(total bet + total raise) / (total bet + total raise + total call + total fold) * 100
stats['V_aggressionFreqWA']= 0.0

stats['V_seenFlopCount'] = 0#How often player has made it to the flop
stats['V_seenFlopRate'] = []
stats['V_seenFlopRateWA']= 0.0

stats['V_seenTurnCount'] = 0#How often player has made it to the flop
stats['V_seenTurnRate'] = []
stats['V_seenTurnRateWA']= 0.0

stats['V_FlopCbetCount'] = 0#How often player has bets as a raise ("ARR" stands for all reraises)
stats['V_FlopCbetRate'] = []
stats['V_FlopCbetRateWA']= 0.0

stats['V_TurnCbetCount'] = 0#How often player makes a continuation bet after the first one ("ARRR" stands for all rereraises)
stats['V_TurnCbetRate'] = []
stats['V_TurnCbetRateWA'] = 0.0

stats['V_ftoFlopCbetCount'] = 0#How often player folds to all reraises
stats['V_ftoFlopCbetRate'] = []
stats['V_ftoFlopCbetRateWA'] = 0.0

stats['V_ftoTurnCbetCount'] = 0#How often player folds to all rereraises
stats['V_ftoTurnCbetRate'] = []
stats['V_ftoTurnCbetRateWA'] = 0.0

#General Statistics
stats['V_BetCount'] = 0
stats['V_CallCount'] = 0
stats['V_RaiseCount'] = 0
stats['V_FoldCount'] = 0
stats['AverageVPIPAll'] = 0.0
stats['StdDevVPIPAll'] = 0.0
stats['HigherVPIPRate'] = []
stats['HighVPIPRate'] = []
stats['HigherVPIPCount'] = 0
stats['HighVPIPCount'] =0
stats['HigherVPIPRateWA'] = 0.0
stats['HighVPIPRateWA'] = 0.0
stats['TotVPIPAll'] = []
stats['CountVPIPAll'] = 0

aggressiveEvents = ['V_pfrRate','V_vpipRate','V_3betRate','V_seenFlopRate','V_seenTurnRate','V_FlopCbetRate','V_TurnCbetRate']


def update(lastActions,myName,oppName):
	for i in range(len(lastActions)):
		lastActions[i] = lastActions[i].split(':')
	outcome = lastActions[-1]
	
	stats['numHandsPlayed']+=1
	if outcome[-1] == myName:
		stats['winCount']+=1
		stats['winAverage'].append(int(outcome[1])/float(stats['winCount']))
		stats['winRate'] = stats['winCount']/float(stats['numHandsPlayed'])

	else:
		stats['loseAverage'].append(int(outcome[1])/float(stats['numHandsPlayed']-stats['winCount']))
	#Break up rounds into lists
	#Pre-flop raise recorder
	for round in lastActions:

		if (round[0] == 'RAISE' and round[-1] == oppName) or (round[0] == 'BET' and round[-1] == oppName):
			stats['V_pfrCount'] += 1
			stats['V_pfrRate'].append(stats['V_pfrCount']/float(stats['numHandsPlayed']))
			
			break
		elif round[0] == 'DEAL':
			break

	#Init fold rate record
	for round in lastActions:
		if (round[0] == 'RAISE' and round[-1] == oppName) or (round[0] == 'CALL' and round[-1] == oppName):
			stats['V_initFoldCount'] += 1
			stats['V_initFoldRate'].append(stats['V_initFoldCount']/float(stats['numHandsPlayed']))
		elif round[0] == 'DEAL':
			#If the don't call or raise during the pre-flop then they folded
			
			break
			

	#Init fold rate record	
	#VPIP recorder
	for round in lastActions:
		if (round[0] == 'RAISE' and round[-1] == oppName) or (round[0] == 'CALL' and round[-1] == oppName) or (round[0] == 'BET' and round[-1] == oppName):

			stats['V_vpipCount'] += 1
			stats['V_vpipRate'].append(stats['V_vpipCount']/float(stats['numHandsPlayed']))
			break
		elif round[0] == 'DEAL':
			#If the don't call or raise during the pre-flop then they folded

			break
	#3bet raise recorder
	for round in lastActions:
		if round[0] == 'RAISE' and round[-1] == oppName:
			stats['V_pfrCount'] += 1
			stats['V_pfrRate'].append(stats['V_pfrCount']/float(stats['numHandsPlayed']))
		else:
			stats['V_initFoldCount'] += 1
			stats['V_initFoldRate'].append(stats['V_initFoldCount']/float(stats['numHandsPlayed']))
			break

	#3bet raise recorder

	#Fold to pfr recorder
	for i in range(len(lastActions)-1):
		if lastActions[i][0] == 'RAISE' and lastActions[i][-1] == myName and lastActions[i+1][0] == 'FOLD':
			stats['V_pfrFoldCount'] += 1
			stats['V_pfrFoldRate'].append(stats['V_pfrFoldCount']/float(stats['numHandsPlayed']))
		elif round[0] == 'DEAL':
			break
	#Fold to 3bet reraise recorder
	for i in range(len(lastActions)-1):
		if lastActions[i][0] == 'RAISE' and lastActions[i][-1] == oppName and lastActions[i+1][0] == 'RAISE' and lastActions[i+2][0] == 'FOLD':
			stats['V_pfrrFoldCount'] += 1
			stats['V_pfrrFoldRate'].append(stats['V_pfrrFoldCount']/float(stats['numHandsPlayed']))
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
			stats['V_seenFlopCount'] += 1
			stats['V_seenFlopRate'].append(stats['V_seenFlopCount']/float(stats['numHandsPlayed']))
			break
	for i in range(len(lastActions)-1):

		if lastActions[i][0] == 'DEAL' and lastActions[i][-1] == 'TURN':
			stats['V_seenTurnCount'] += 1
			stats['V_seenTurnRate'].append(stats['V_seenTurnCount']/float(stats['numHandsPlayed']))
			break
	#Flop C_BET count
	for i in range(len(lastActions)-1):
		if lastActions[i] == ['DEAL','FLOP']:
			for j in range(i,(len(lastActions))):
				if lastActions[j][0] == 'BET' and lastActions[j][-1] == oppName:
					stats['V_FlopCbetCount'] += 1
					stats['V_FlopCbetRate'].append(stats['V_FlopCbetCount']/float(stats['numHandsPlayed']))
				if lastActions[j] == ['DEAL','TURN']:
					break           
			break
	#Turn C_BET count
	for i in range(len(lastActions)-1):
		if lastActions[i] == ['DEAL','TURN']:
			for j in range(i,(len(lastActions))):
				if lastActions[j][0] == 'BET' and lastActions[j][-1] == oppName:
					stats['V_TurnCbetCount'] += 1
					stats['V_TurnCbetRate'].append(stats['V_TurnCbetCount']/float(stats['numHandsPlayed']))            
			break
	for i in range(len(lastActions)-1):
		if lastActions[i] == ['DEAL','FLOP']:
			for j in range(i,(len(lastActions))):
				if lastActions[j][0] == 'BET' and lastActions[j][-1] == myName:
					if lastActions[j+1][0] == 'FOLD' and lastActions[j+1][-1] == oppName:
						stats['V_ftoFlopCbetCount'] += 1
						stats['V_ftoFlopCbetRate'].append(stats['V_ftoFlopCbetCount']/float(stats['numHandsPlayed']))      
					if lastActions[j] == ['DEAL','RIVER']:
						break     
			break
	for i in range(len(lastActions)-1):
		if lastActions[i] == ['DEAL','TURN']:
			for j in range(i,(len(lastActions))):
				if lastActions[j][0] == 'BET' and lastActions[j][-1] == myName:
					if lastActions[j+1][0] == 'FOLD' and lastActions[j+1][-1] == oppName:
						stats['V_ftoTurnCbetCount'] += 1
						stats['V_ftoTurnCbetRate'].append(stats['V_ftoTurnCbetCount']/float(stats['numHandsPlayed']))            
			break
   
	for round in lastActions:
		if (round[0] == 'RAISE' and round[-1] == oppName) or (round[0] == 'BET' and round[-1] == oppName):
			stats['TotVPIPAll'].append(int(round[1]))

	stats['AverageVPIPAll'] = sum(stats['TotVPIPAll'])/float(stats['numHandsPlayed'])
	squarevariance = 0
	for x in stats['TotVPIPAll']:		
			squarevariance += ((x - stats['AverageVPIPAll'])**2)
	try:
		stats['StdDevVPIPAll'] = math.sqrt(squarevariance/len(stats['TotVPIPAll']))
	except ZeroDivisionError:
		stats['StdDevVPIPAll'] = 0

	for round in lastActions:
		if (round[0] == 'RAISE' and round[-1] == oppName) or (round[0] == 'BET' and round[-1] == oppName):
			if (int(round[1]) >= stats['AverageVPIPAll'] + stats['StdDevVPIPAll']):
				stats['HighVPIPCount'] += 1
				stats['HighVPIPRate'].append(stats['HighVPIPCount']/float(stats['numHandsPlayed']))
	for round in lastActions:
		if (round[0] == 'RAISE' and round[-1] == oppName) or (round[0] == 'BET' and round[-1] == oppName):
			if (int(round[1]) >= stats['AverageVPIPAll'] + stats['StdDevVPIPAll']*1.5):
				stats['HigherVPIPCount'] += 1
				stats['HigherVPIPRate'].append(stats['HigherVPIPCount']/float(stats['numHandsPlayed']))
	CalculateWAs = ['winAverage','loseAverage','V_pfrRate','V_vpipRate','V_initFoldRate','V_pfrFoldRate','V_pfrrFoldRate',
	'V_aggressionFactor','V_aggressionFreq','V_seenFlopRate','V_seenTurnRate','V_FlopCbetRate',
	'V_TurnCbetRate','V_ftoFlopCbetRate','V_ftoTurnCbetRate']

	for stat in CalculateWAs:
		count = 0
		for x in stats[stat][::-1]:
			stats[stat+'WA'] = (x*0.993**count)/float(len(stats[stat]))
			count+=1



	try:
		stats['V_aggressionFactor'].append((stats['V_BetCount'] + stats['V_RaiseCount'])/float(stats['V_CallCount']))
	except ZeroDivisionError:
		stats['V_aggressionFactor'].append(0)
	try:
		stats['V_aggressionFreq'].append((stats['V_BetCount'] + stats['V_RaiseCount'])/float(stats['V_RaiseCount'] + stats['V_FoldCount'] + stats['V_CallCount'] + stats['V_BetCount']))
	except ZeroDivisionError:
		stats['V_aggressionFreq'].append(0)

def display_stats():
	return stats  