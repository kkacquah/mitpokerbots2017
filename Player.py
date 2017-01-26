import argparse
import socket
import sys
import prefloplogic as preflop
import historian as hist
import strategy as strat
"""
Simple example pokerbot, written in python.

This is an example of a bare bones pokerbot. It only sets up the socket
necessary to connect with the engine and then always returns the same action.
It is meant as an example of how a pokerbot should communicate with the engine.

PocketAces v0.1a
"""

class Player:
        
    def run(self, input_socket):
        firstround = True
        # Get a file-object for reading packets from the socket.
        # Using this ensures that you get exactly one packet per read.
        f_in = input_socket.makefile()
        lastActions = None
        while True:
            
            # Block until the engine sends us a packet
            
            data = f_in.readline().strip().split()
            # If data is None, connection has closed.
            if not data:
                print "Gameover, engine disconnected."
                break

            # Here is where you should implement code to parse the packets from
            # the engine and act on it. We are just printing it instead.
            print data

            # When appropriate, reply to the engine with a legal action.
            # The engine will ignore all spurious responses.
            # The engine will also check/fold for you if you return an
            # illegal action.
            # When sending responses, terminate each response with a newline
            # character (\n) or your bot will hang!
            word = data[0]
            
            if word == 'NEWGAME':
                myName = data[1]
                
                bigblind = data[4]
                totalHands = data[5]
                timeBank = data[6]
                print 'NEWGAME start'
                print 'my name is:' + myName
                print bigblind
                print totalHands
                print timeBank
                
            elif word == 'NEWHAND':
                handId = data[1] # number hand (1-1000)
                button = data[2] #small blind (True/False) -> act firt preflop then second
                myHand = [data[3],data[4]]
                profits = data[5]
                #timeBank = data[7]
                print 'my hand is:' + str(myHand)
                print hist.display_stats()
    
            elif word == "GETACTION":
                
                print 'data is: ' + str(data)
                numBoardCards = int(data[2])
                boardCards = []
                for i in range(0,numBoardCards):
                    boardCards.append(data[3+i])
                
                print 'boardCards is ' + str(boardCards)
                
                numLastActions = int(data[3+numBoardCards])
                lastActions = []
                for i in range(0,numLastActions):
                    lastActions.append(data[4+numBoardCards+i])
                    
                print 'last are ' + str(lastActions)
                switched = False
        
                for i in range(0,len(lastActions)): #check if I discarded
                    if lastActions[i].find('DISCARD:') != -1 and lastActions[i].find(myName) != -1:
                        switched = True
                        break;
                
                if switched:
                    discardAction = lastActions[i]
                    if discardAction.count(':') == 3: #shows it was this robot that switched
                        #DISCARD:oo:NN:Player..
                        oldCard = discardAction[8:10]
                        newCard = discardAction[11:13]
                        myHand[myHand.index(oldCard)] = newCard
                
                
                numLegalActions = int(data[4+numBoardCards+numLastActions])
                legalActions = []
                for i in range(0,numLegalActions):
                    legalActions.append(data[5+numBoardCards+numLastActions+i])
                print 'legal are ' + str(legalActions)
                print 'my hand is: ' + str(myHand)
                
                action = 'CHECK\n'
                history = hist.display_stats()
                
                #if numBoardCards == 0 : #preflop
                 #   action = preflop.getaction(myHand,data)
                #else:
                action = strat.getAction(myHand,boardCards,legalActions,lastActions,history,switched,button)
                    
                s.send(action)
                
            elif word == "HANDOVER":
                PandL = int(data[2])
                #indicates the conclusion of the current hand
                numBoardCards = int(data[3])
                numLastActions = 0
                boardCards = []
                for i in range(numBoardCards):
                    boardCards.append(data[4+i])
                    numLastActions = int(data[4+numBoardCards])
                #Collect last actions, the packet wasn't returning all of them
                lastActions = []
                for i in range(0,numLastActions):
                    lastActions.append(data[5+numBoardCards+i])
                    print lastActions
                #hist.update(lastActions)                    
                history = hist.display_stats()    
                timeBank = data[5+numBoardCards+numLastActions]   
                
            #elif word == "KEYVALUE" :
                #key = data[1]
                #value = data[2]
                #now store/ use this somehow
    
            elif word == "REQUESTKEYVALUES":
                # At the end, the engine will allow your bot save key/value pairs.
                # Send FINISH to indicate you're done.
                
                #s.send("PUT key value") #for each pair
                s.send("FINISH\n")
            else:
                s.send("FINISH\n")
                
        # Clean up the socket.
        s.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Pokerbot.', add_help=False, prog='pokerbot')
    parser.add_argument('-h', dest='host', type=str, default='localhost', help='Host to connect to, defaults to localhost')
    parser.add_argument('port', metavar='PORT', type=int, help='Port on host to connect to')
    args = parser.parse_args()

    # Create a socket connection to the engine.
    print 'Connecting to %s:%d' % (args.host, args.port)
    try:
        s = socket.create_connection((args.host, args.port))
    except socket.error as e:
        print 'Error connecting! Aborting'
        exit()

    bot = Player()
    bot.run(s)
