#Historian Class
numHandsPlayed= 0 #Hands Played so far
winCount = 0 #Your win rate
#Pre-Flop Statistics
prefstats = dict()
#A prefix of V_ denotes the villain, a prefix of H_ denotes the hero
prefstats['V_pfrCount']= 0#pre-flop raise
prefstats['H_pfrCount'] = 0
prefstats['V_vpipCount'] = 0#call or raise pre-flop
prefstats['H_vpipCount'] = 0
prefstats['V_initFoldCount'] = 0#related to vpip, counts when they don't play their hand
prefstats['H_pipCount'] = 0
prefstats['V_ThreeBCount'] = 0#How many times the opponent 3-bet
prefstats['H_ThreeBCount'] = 0
prefstats['V_pfrFoldCount'] = 0#Fold to initial pre-flop raise
prefstats['H_pfrFoldCount'] = 0
prefstats['V_pfrrFoldCount'] = 0#Fold to Pre-flop Re-raise
#Post-Flop Statistics
postfstats = dict
postfstats['H_aggressionFactor']= 0 #(Bet + Raise) / Call
postfstats['V_aggressionFactor']= 0
postfstats['H_aggressionFreq']= 0#(total bet + total raise) / (total bet + total raise + total call + total fold) * 100
postfstats['V_aggressionFreq']= 0
postfstats['H_betCount'] = 0#Number of times a player bets
postfstats['V_betCount'] = 0
postfstats['H_callCount'] = 0#Number of times a player calls
postfstats['V_callCount'] = 0
postfstats['H_wtsdCount'] = 0#How often player goes to showdown after seeing flop (can be used with aggression)
postfstats['V_wtsdCount'] = 0
postfstats['H_showdownCount'] = 0#How often player goes to showdown in total
postfstats['V_showdownCount'] = 0
postfstats['H_seenFlopCount'] = 0#How often player has made it to the flop
postfstats['V_seenFlopCount'] = 0
postfstats['H_CBCount'] = 0#How often player has bets as a preflop raiser
postfstats['V_CBCount'] = 0
postfstats['H_TwoCBCount'] = 0#How often player makes a continuation bet after the first one
postfstats['V_TwoCBCount'] = 0
postfstats['H_ftoCBCount'] = 0#How often player folds to CBet
postfstats['V_ftoCBCount'] = 0
postfstats['H_ftoTwoCBCount'] = 0#How often player folds to second Cbet
postfstats['V_ftoTwoCBCount'] = 0

def update(lastActions):
    lastActions = lastActions.split()