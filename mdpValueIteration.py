# -*- coding: utf-8 -*-
"""
***********************************************
* LSINF2275 : Data mining and decision making *
* ------------------------------------------- *
*                                             *
*      MDP solving with value iteration       *
*            Project #1, 2021                 *
*                                             *
***********************************************

@author:    Gabriel BAILLY 
            Lara WAUTIER
            Corentin ZONE

@program:   DATS2M

@group:     nº8 

"""

import numpy as np

def Next(square, throw, circle):
    """
    Inputs:
        - square : the current square when dice is thrown.
        - throw : the result of throwing the dice (can be +0, +1, +2 or +3).
        - circle : if you must land on square 15 to win.
    --------------------------------------------------------------------------
    Outputs:
        - numeric value to determine the next square (from 0 to 14)
    """
    
    # square 3 is the only one which can lead to two different squares ; we manage it separately in the value iteration. 
    if square != 2 : 
        
        # circle rule does NOT APPLY
        if circle == False:
            if square < 7:
                return square+throw
            
            elif square in range(7,10):     # slow lane
                if square+throw >= 10:
                    return 14
                else:
                    return square+throw
                
            elif square in range(10,14):    # fast lane
                if square+throw >= 14:
                    return 14
                else:
                    return square+throw
        
        # circle rule DOES APPLY
        else:
            if square < 7:
                return square+throw
            
            elif square in range(7,10):     # slow lane
                if square+throw <= 9:
                    return square+throw
                elif square+throw == 10:
                    return 14
                elif square+throw > 10:
                    return square-11+throw
                
            elif square in range(10,14):    # fast lane
                if square+throw <= 14:
                    return square+throw
                else:
                    return square-15+throw



def getTrapped(square, trap, V):
    """
    Inputs:
        - square : square you land on
        - trap : type of trap (0 = no trap, 1:4 are traps defined in the guidelines)
    Outputs:
        - numeric value of the new square, taking the effect of the trap in account.
    """
    # Square is NOT a trap
    if trap == 0:
        return square
    
    # Square IS a trap
    if trap == 1:                   # Trap 1 : return to square 1
        return 0
    
    elif trap == 2:                 # Trap 2 : go 3 squares backwards
        if square < 3:
            return 0
        elif square < 10:
            return square-3
        elif square >= 10:
            return square-10
        
    elif trap == 3:                 # Trap 3 : skip next turn
        return square
        
    elif trap == 4:                 # Trap 4 : teleports you anywhere on the board, with equiprobability
        newV = 0                    # We had to V the sum( _k = 1 ^to 15 ) of { 1/15 * V(k) }
        for k in range(15):
            newV += (1/15)*V[k]
        return newV






def valueIteration(V, k, a, layout, circle):
    """
    Inputs:
        - V : vector of expected values for each square, to be updates.
        - k : current square.
        - a : action (secure, normal or risky dice).
        - layout : traps layout.
        - circle : if you must land on square 15 to win.
    -------------------------------------------------------------------
    Outputs:
        - newV : the updated vector of expected values for each square.
    """
    # define k+1 , k+2 and k+3 to make function faster.
    k1 = Next(k, 1, circle)
    k2 = Next(k, 2, circle)
    k3 = Next(k, 3, circle)
    
    # assign variables to sum with immediate cost.
    pVk = 0
    pVk1 = 0
    pVk2 = 0
    pVk3 = 0
    
    pVk1s = 0       # if slow lane when square 3
    pVk2s = 0
    pVk3s = 0
    
    pVk1f = 0       # if fast lane when square 3
    pVk2f = 0
    pVk3f = 0
    
    #--------------------------------
    # DICE 1 , doesn't trigger traps.
    #--------------------------------
    if a == 1:
        if k != 2:
            return 1 + (1/2)*V[k] + (1/2)*V[k1]                     # we have V(k) for a = a_1
        else:
            return 1 + (1/2)*V[2] + ( (1/4)*V[3] + (1/4)*V[10] )    # we have V(k) for a = a_1 --- if 2 possible lanes
        
    
    #--------------------------------------------
    # DICE 2, 1/2 chance of triggering the traps.
    #--------------------------------------------
    elif a == 2:
        # *** square 3 treated appart for simplicty
        if k != 2:
            # manage square k
            if layout[k] == 0:
                pVk = (1/3)*V[k]
            elif layout[k] == 1:
                pVk = (1/3)*( (1/2)*V[k] + (1/2)*V[getTrapped(k, 1, V)] )
            elif layout[k] == 2:
                pVk = (1/3)*( (1/2)*V[k] + (1/2)*V[getTrapped(k, 2, V)] )
            elif layout[k] == 3:
                pVk = (1/3)*( (1/2)*V[k] + (1/2)*(1 + V[getTrapped(k, 3, V)]) )
            elif layout[k] == 4:
                pVk = (1/3)*( (1/2)*V[k] + (1/2)*(getTrapped(k, 4, V)) )
                
            # manage square k+1  
            if layout[k1] == 0:
                pVk1 = (1/3)*V[k1]
            elif layout[k1] == 1:
                pVk1 = (1/3)*( (1/2)*V[k1] + (1/2)*V[getTrapped(k1, 1, V)] )
                
            elif layout[k1] == 2:
                pVk1 = (1/3)*( (1/2)*V[k1] + (1/2)*V[getTrapped(k1, 2, V)] )
                
            elif layout[k1] == 3:
                pVk1 = (1/3)*( (1/2)*V[k1] + (1/2)*(1 + V[getTrapped(k1, 3, V)]) )
                
            elif layout[k1] == 4:
                pVk1 = (1/3)*( (1/2)*V[k1] + (1/2)*(getTrapped(k1, 4, V)) )
                
            # manage square k+2
            if layout[k2] == 0:
                pVk2 = (1/3)*V[k2]
            elif layout[k2] == 1:
                pVk2 = (1/3)*( (1/2)*V[k2] + (1/2)*V[getTrapped(k2, 1, V)] )
                
            elif layout[k2] == 2:
                pVk2 = (1/3)*( (1/2)*V[k2] + (1/2)*V[getTrapped(k2, 2, V)] )
                
            elif layout[k2] == 3:
                pVk2 = (1/3)*( (1/2)*V[k2] + (1/2)*(1 + V[getTrapped(k2, 3, V)]) )
                
            elif layout[k2] == 4:
                pVk2 = (1/3)*( (1/2)*V[k2] + (1/2)*(getTrapped(k2, 4, V)) )
        
        
            return ( 1 + pVk + pVk1 + pVk2 )                                           # finaly we have V(k) for a = a_2
        
        
        # *** square 3, we directly put the square number (-1 for index) for simplicity and readability                   
        else:
            # manage square 3
            if layout[2] == 0:
                pVk = (1/3)*V[2]
            elif layout[2] == 1:
                pVk = (1/3)*( (1/2)*V[2] + (1/2)*V[getTrapped(2, 1, V)])
                
            elif layout[2] == 2:
                pVk = (1/3)*( (1/2)*V[2] + (1/2)*V[getTrapped(2, 2, V)])
                
            elif layout[2] == 3:
                pVk = (1/3)*( (1/2)*V[2] + (1/2)*(1+V[getTrapped(2, 3, V)]))
                
            elif layout[2] == 4:
                pVk = (1/3)*( (1/2)*V[2] + (1/2)*(getTrapped(2, 4, V)))
                
        # SLOW LANE
        # *********
            # manage square 4
            if layout[3] == 0:
                pVk1s = (1/6)*V[3]
            elif layout[3] == 1:
                pVk1s = (1/6)*( (1/2)*V[3] + (1/2)*V[getTrapped(3, 1, V)])
                
            elif layout[3] == 2:
                pVk1s = (1/6)*( (1/2)*V[3] + (1/2)*V[getTrapped(3, 2, V)])
                
            elif layout[3] == 3:
                pVk1s = (1/6)*( (1/2)*V[3] + (1/2)*(1+V[getTrapped(3, 3, V)]))
                
            elif layout[3] == 4:
                pVk1s = (1/6)*( (1/2)*V[3] + (1/2)*(getTrapped(3, 4, V)))
        
            # manage square 5
            if layout[4] == 0:
                pVk2s = (1/6)*V[4]
            elif layout[4] == 1:
                pVk2s = (1/6)*( (1/2)*V[4] + (1/2)*V[getTrapped(4, 1, V)])
                
            elif layout[4] == 2:
                pVk2s = (1/6)*( (1/2)*V[4] + (1/2)*V[getTrapped(4, 2, V)])
                
            elif layout[4] == 3:
                pVk2s = (1/6)*( (1/2)*V[4] + (1/2)*(1+V[getTrapped(4, 3, V)]))
                
            elif layout[4] == 4:
                pVk2s = (1/6)*( (1/2)*V[4] + (1/2)*(getTrapped(4, 4, V)))
            
        # FAST LANE
        # *********
            # manage square 11
            if layout[10] == 0:
                pVk1f = (1/6)*V[10]
            elif layout[10] == 1:
                pVk1f = (1/6)*( (1/2)*V[10] + (1/2)*V[getTrapped(10, 1, V)])
                
            elif layout[10] == 2:
                pVk1f = (1/6)*( (1/2)*V[10] + (1/2)*V[getTrapped(10, 2, V)])
                
            elif layout[10] == 3:
                pVk1f = (1/6)*( (1/2)*V[10] + (1/2)*(1+V[getTrapped(10, 3, V)]))
                
            elif layout[10] == 4:
                pVk1f = (1/6)*( (1/2)*V[10] + (1/2)*(getTrapped(10, 4, V)))
        
            # manage square 12
            if layout[11] == 0:
                pVk2f = (1/6)*V[11]
            elif layout[11] == 1:
                pVk2f = (1/6)*( (1/2)*V[11] + (1/2)*V[getTrapped(11, 1, V)])
                
            elif layout[11] == 2:
                pVk2f = (1/6)*( (1/2)*V[11] + (1/2)*V[getTrapped(11, 2, V)])
                
            elif layout[11] == 3:
                pVk2f = (1/6)*( (1/2)*V[11] + (1/2)*(1+V[getTrapped(11, 3, V)]))
                
            elif layout[11] == 4:
                pVk2f = (1/6)*( (1/2)*V[11] + (1/2)*(getTrapped(11, 4, V)))
            
            return ( 1 + pVk + pVk1s + pVk2s + pVk1f + pVk2f )                         # finaly we have V(k) for a = a_2 --- if 2 possible lanes
        
    #-------------------------------      
    # DICE 3, always triggers traps.
    #-------------------------------
    elif a == 3:
        # *** square 3 treated appart for simplicty
        if k != 2:
            # manage square k
            if layout[k] == 0:
                pVk = (1/4)*V[k]
            elif layout[k] == 1:
                pVk = (1/4)*V[getTrapped(k, 1, V)] 
            elif layout[k] == 2:
                pVk = (1/4)*V[getTrapped(k, 2, V)] 
            elif layout[k] == 3:
                pVk = (1/4)*(1 + V[getTrapped(k, 3, V)] ) 
            elif layout[k] == 4:
                pVk = (1/4)*(getTrapped(k, 4, V))
                
            # manage square k+1 
            if layout[k1] == 0:
                pVk1 = (1/4)*V[k1]
            elif layout[k1] == 1:
                pVk1 = (1/4)*V[getTrapped(k1, 1, V)] 
            elif layout[k1] == 2:
                pVk1 = (1/4)*V[getTrapped(k1, 2, V)] 
            elif layout[k1] == 3:
                pVk1 = (1/4)*(1 + V[getTrapped(k1, 3, V)] ) 
            elif layout[k1] == 4:
                pVk1 = (1/4)*(getTrapped(k1, 4, V))
                
            # manage square k+2
            if layout[k2] == 0:
                pVk2 = (1/4)*V[k2]
            elif layout[k2] == 1:
                pVk2 = (1/4)*V[getTrapped(k2, 1, V)] 
            elif layout[k2] == 2:
                pVk2 = (1/4)*V[getTrapped(k2, 2, V)] 
            elif layout[k2] == 3:
                pVk2 = (1/4)*(1 + V[getTrapped(k2, 3, V)] ) 
            elif layout[k2] == 4:
                pVk2 = (1/4)*(getTrapped(k2, 4, V))
                
            # manage square k+3
            if layout[k3] == 0:
                pVk3 = (1/4)*V[k3]
            elif layout[k3] == 1:
                pVk3 = (1/4)*V[getTrapped(k3, 1, V)] 
            elif layout[k3] == 2:
                pVk3 = (1/4)*V[getTrapped(k3, 2, V)] 
            elif layout[k3] == 3:
                pVk3 = (1/4)*(1 + V[getTrapped(k3, 3, V)] ) 
            elif layout[k3] == 4:
                pVk3 = (1/4)*(getTrapped(k3, 4, V))
    
            return ( 1 + pVk + pVk1 + pVk2 + pVk3 )                                   # finaly we have V(k) for a = a_3 
        
        # *** square 3, we directly put the square number (-1 for index) for simplicity and readability                  
        else:
            # manage square 3
            if layout[2] == 0:
                pVk = (1/4)*V[2]
            
            elif layout[2] == 1:
                pVk = (1/4)*V[getTrapped(2, 1, V)]
                
            elif layout[2] == 2:
                pVk = (1/4)*V[getTrapped(2, 2, V)]
                
            elif layout[2] == 3:
                pVk = (1/4)*(1+V[getTrapped(2, 3, V)])
                
            elif layout[2] == 4:
                pVk = (1/4)*(getTrapped(2, 4, V))
                
        # SLOW LANE
        # *********
            # manage square 4
            if layout[3] == 0:
                pVk1s = (1/8)*V[3]
            
            elif layout[3] == 1:
                pVk1s = (1/8)*V[getTrapped(3, 1, V)]
                
            elif layout[3] == 2:
                pVk1s = (1/8)*V[getTrapped(3, 2, V)]
                
            elif layout[3] == 3:
                pVk1s = (1/8)*(1+V[getTrapped(3, 3, V)])
                
            elif layout[3] == 4:
                pVk1s = (1/8)*(getTrapped(3, 4, V))
        
            # manage square 5
            if layout[4] == 0:
                pVk2s = (1/8)*V[4]
            
            elif layout[4] == 1:
                pVk2s = (1/8)*V[getTrapped(4, 1, V)]
                
            elif layout[4] == 2:
                pVk2s = (1/8)*V[getTrapped(4, 2, V)]
                
            elif layout[4] == 3:
                pVk2s = (1/8)*(1+V[getTrapped(4, 3, V)])
                
            elif layout[4] == 4:
                pVk2s = (1/8)*(getTrapped(4, 4, V))
                
            # manage square 6
            if layout[5] == 0:
                pVk3s = (1/8)*V[5]
            
            elif layout[5] == 1:
                pVk3s = (1/8)*V[getTrapped(5, 1, V)]
                
            elif layout[5] == 2:
                pVk3s = (1/8)*V[getTrapped(5, 2, V)]
                
            elif layout[5] == 3:
                pVk3s = (1/8)*(1+V[getTrapped(5, 3, V)])
                
            elif layout[5] == 4:
                pVk3s = (1/8)*(getTrapped(5, 4, V))
            
        # FAST LANE
        # *********
            # manage square 11
            if layout[10] == 0:
                pVk1f = (1/8)*V[10]
            
            elif layout[10] == 1:
                pVk1f = (1/8)*V[getTrapped(10, 1, V)]
                
            elif layout[10] == 2:
                pVk1f = (1/8)*V[getTrapped(10, 2, V)]
                
            elif layout[10] == 3:
                pVk1f = (1/8)*(1+V[getTrapped(10, 3, V)])
                
            elif layout[10] == 4:
                pVk1f = (1/8)*(getTrapped(10, 4, V))
        
            # manage square 12
            if layout[11] == 0:
                pVk2f = (1/8)*V[11]
            
            elif layout[11] == 1:
                pVk2f = (1/8)*V[getTrapped(11, 1, V)]
                
            elif layout[11] == 2:
                pVk2f = (1/8)*V[getTrapped(11, 2, V)]
                
            elif layout[11] == 3:
                pVk2f = (1/8)*(1+V[getTrapped(11, 3, V)])
                
            elif layout[11] == 4:
                pVk2f = (1/8)*(getTrapped(11, 4, V))
                
            # manage square 13
            if layout[12] == 0:
                pVk3f = (1/8)*V[12]
            
            elif layout[12] == 1:
                pVk3f = (1/8)*V[getTrapped(12, 1, V)]
                
            elif layout[12] == 2:
                pVk3f = (1/8)*V[getTrapped(12, 2, V)]
                
            elif layout[12] == 3:
                pVk3f = (1/8)*(1+V[getTrapped(12, 3, V)])
                
            elif layout[12] == 4:
                pVk3f = (1/8)*(getTrapped(12, 4, V))
            
            return ( 1 + pVk + pVk1s + pVk2s + pVk3s + pVk1f + pVk2f + pVk3f )         # finaly we have V(k) for a = a_3 --- if 2 possible lanes
                     
    
def markovDecision(layout, circle):
    """ 
    Determines the optimal strategy of a Snakes and Ladders game.
    -------------------------------------------------------------
    Inputs :
        - layout : numpy array. 
                   layout of the traps on the board (see report appendices)
        - circle : boolean.
                   if True, you have to land exactly on square 15 to win, 
                   otherwise you restart from the beginning.
    -------------------------------------------------------------
    Outputs :
        - Expec : numpy array. 
                  expected number of turns at case i in 1:15, if optimal policy is used.
        - Dice : numpy array.
                 optimal dice for each square, given the layout.
    """     
    V = np.zeros(15)
    policy = np.zeros(14)
    theta = 0.00001         # maximal difference between V(k_{it-1}) and V(k_{it})
    end = False             # will be true when every state has converged
    
    iterCount = 0
    
    while not end:          # until every iterated values are close enough to previous iteration
    
        validSquares = 0    # no square has converged at the beginning    
    
        for k in range(13,-1,-1):
            
            v = V[k]        # stock previous expected values to compare if difference is small enough    

            # stock value iteration for the 3 dices at square k
            choice1 = valueIteration(V, k, 1, layout, circle)
            choice2 = valueIteration(V, k, 2, layout, circle)
            choice3 = valueIteration(V, k, 3, layout, circle)
            
            # which action has the smallest expected number of turns ?
            V[k] = min(choice1, choice2, choice3)           

            if V[k] == choice1:     # it's the dice 1 , stock it
                policy[k] = 1
            elif V[k] == choice2:   # it's the dice 2 , stock it
                policy[k] = 2
            elif V[k] == choice3:   # it's the dice 3 , stock it
                policy[k] = 3
                
            iterCount += 1
                
            delta = abs(v - V[k])       # update difference with previous expected value
            if delta < theta:           # check if updated difference is small enough, if yes the square is valid
                validSquares += 1       
                
        # we got through the 14 squares, end for.
        if validSquares == 14:          # did they all converge ? if yes, end while.
            end = True
            
    # we're done ! now just give the outputs their proper names.
    Expec = V[0:14]      # Stock Expec vector of expected turns V(k) for optimal policy; 
    Dice = policy  # Stock Dice vector of optimal policy pi(k)
     
    return [Expec, Dice]


"""
Some basic test
---------------

layoutSimple = np.array([0,1,1,1,4,\
                         4,0,0,0,0,\
                         4,4,0,0,0])

print("Layout to be tested:\n\n", layoutSimple, "\n")
    
print("Check MDP if circle=False:\n")
opt = markovDecision(layoutSimple, False)
print(opt, "\n")

print("Check MDP if circle=True\n")
opt = markovDecision(layoutSimple, True)
print(opt, "\n")

layout=[0,1,0,0,3,0,4,2,0,0,4,2,0,0,0]
print("Check MDP if circle=False:\n")
opt = markovDecision(layout, False)
print(layout)
print(opt[1], "\n")
print(opt[0], "\n")

print("Check MDP if circle=True\n")
opt = markovDecision(layout, True)
print(opt[1], "\n")

layout=[0,4,4,4,4,4,4,4,4,4,4,4,4,4,0]
print("Check MDP if circle=True\n")
opt = markovDecision(layout, False)
print(opt[1], "\n")

layout=[0,1,0,0,3,0,4,2,0,4,4,2,0,4,0]
print("Check MDP if circle=True\n")
opt = markovDecision(layout, False)
print(opt[1], "\n")

layout=[0,1,0,2,3,0,2,0,1,0,4,2,0,4,0]
print("Check MDP if circle=False\n")
opt = markovDecision(layout, False)
print(opt, "\n")

print("Check MDP if circle=True\n")
opt = markovDecision(layout, True)
print(opt, "\n")
"""