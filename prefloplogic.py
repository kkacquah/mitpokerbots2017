# array matching index (strength) to numerical value
master_array = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
# pythonic hack to determine if an input string is an integer
def test(s):
    try:
        return int(s)
    except ValueError:
        return -1
# function that returns the index of the numLegalActions element of the packet, 
# using the observation that numLegalActions is always the fourth integer in the GETACTION packet.
def splitPacket(data):
	packet = data
	counter = 0
	for i in range(len(packet)):
		if test(packet[i])>=0:
			counter+=1
		if counter == 4:
			return i
	return None

# function that takes data packet and potential legal action, and determines
# whether said action is legal. Gives index of that action within packet, or -1 if not legal.
def canIDoThis(action,data):
	packet = data
	index = -1
	for i in range(splitPacket(data),len(packet)):
		if packet[i][0:len(action)]==action:
			index = i
	return index
# preflop strategy that goes all in on a pocket pair or high card (T,J,Q,K,A in hand) and checkfolds otherwise
def getaction(myHand,data):
	firstNum = myHand[0][0]
	firstSuit = myHand[0][1]
	secondNum = myHand[1][0]
	secondSuit = myHand[1][1]
	
	if firstNum == secondNum or max(master_array.index(firstNum),master_array.index(secondNum))>7:
		#print 'I GOT A PAIR!!! OR HAD A HIGH CARD !!1!!!!!11! or both'
		if canIDoThis('BET',data)>-1:
			# next line splits BET:minBet:maxBet action into its components,
			# then extracts the maxBet so we can go all in
			maxBet = data[canIDoThis('BET',data)].split(':')[2]
			#return 'BET:'+maxBet+'\n'
		elif canIDoThis('RAISE',data)>-1:
			maxRaise = data[canIDoThis('RAISE',data)].split(':')[2]
			#return 'RAISE:'+maxRaise+'\n'
		if canIDoThis('CALL',data)>-1:
			return 'CALL\n'
		else: 
			return 'CHECK\n'
	return 'CHECK\n'