# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 18:49:02 2021

@author: Corentin ZONE
         Gabriel BAILLY
         Lara WAUTIER
"""

import random
import itertools

def security_dice():
    return random.randrange(0, 2)


def normal_dice():
    return random.randrange(0, 3)


def risky_dice():
    return random.randrange(0, 4)


def moving():
    dice = random.randrange(0, 3)
    if dice == 0:   #safe dice
        end = security_dice()
    if dice == 1:   #normal dice
        end = normal_dice()
    if dice == 2:    #risky dice
        end = risky_dice()
    return (dice,end)


def trap(type,pos_start,turn):
    if type==1:   #trap 1 "restart": restart
        pos_end=0

    elif type==2:  #trap 2 "Penalty": 3 squares backwards
        #case when come from the fast lane
        if pos_start==10:
            pos_end=0
        elif pos_start==11:
            pos_end=1
        elif pos_start==12:
            pos_end=2
        #normal case
        else:
            pos_end = pos_start - 3
            if pos_end<0:
                pos_end=0

    elif type==3:   #trap 3 "Prison": wait 1 turn
        pos_end=pos_start
        turn+=1

    else:          #trap 4 "Gamble": randomly teleported
        pos_end=random.randrange(0,14)

    return [pos_end,turn]


def game(layout,circle,strategy):
    pos=0
    out=[]
    turn=0

    while pos<14:
        turn += 1
        #selection of the strategy for the game
        if strategy==0:
            dice_roll=(0,security_dice())
        elif strategy==1:
            dice_roll=(1,normal_dice())
        elif strategy==2:
            dice_roll=(2,risky_dice())
        else:
            dice_roll=moving()

        #choice of the lane and progress in the game
        if pos==2 and dice_roll[1]!=0:  #choice of the lane
            proba = random.randrange(0,2)
            if proba==0:   #fast lane
                pos=dice_roll[1]+pos+7
            else:         #slow lane
                pos=dice_roll[1]+pos
        elif pos==9 and dice_roll[1]!=0:   #arrive from the slow lane
            pos=pos+dice_roll[1]+4
        else:
            pos=dice_roll[1]+pos

        #if circle game, come back to the start
        if pos>14 and circle:
            pos=pos-15

        #code for triggering trap
        triggering="No"
        if pos<14:
            trap_at_pos = layout[pos]
            #100% triggering trap with risky dice
            if layout[pos]!=0  and dice_roll[0]==2:
                pos=trap(layout[pos],pos,turn)[0]
                turn=trap(layout[pos],pos,turn)[1]
                triggering="Yes"

            #50% triggering with normal dice
            elif layout[pos]!=0 and dice_roll[0]==1:
                triggering_proba=random.randrange(0,2)
                if triggering_proba==1:
                    pos = trap(layout[pos], pos, turn)[0]
                    turn = trap(layout[pos], pos, turn)[1]
                    triggering="yes"
        else:
            trap_at_pos=0    #case when reach exactly the end or exceeds if no circle game

        out.append((dice_roll[0],dice_roll[1],pos,trap_at_pos,triggering,turn))
    return out

layout=[0,1,0,0,3,0,4,2,0,0,4,2,0,0]
#layout=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
result=game(layout,True,3)
print(result)

table="Dice   Value   position   trap  triggered  nb_turn"
for i in range(0,len(result)):
    table+="\n{:^5}  {:^5}     {:^5}   {:^5}    {:^5}    {:^5} ".format(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],result[i][5])
print(table)


def summary(layout,circle,strategy,iteration):
    """
    :param layout: vector of trap's type per case
    :param circle: boolean, describe if cicle game
    :param strategy: int, describe the strategy (0, only safe dice; 1, only normal dice; 2, only risky dice; 3, random choice)
    :param iteration: int, number of iteration to make
    :return: float, average (expected) number of turn to end this setting of the game
    """
    stop=0
    total_turn=0
    while stop<iteration:
        result=game(layout,circle,strategy)
        total_turn+=result[len(result)-1][5]
        stop+=1
    return total_turn/iteration

ite=100
print("Expected turns for random and no circle: "+ str(summary(layout,False,3,ite)))
print("Expected turns for random and circle: "+ str(summary(layout,True,3,ite)))
print("Expected turns for safe and no circle: "+ str(summary(layout,False,0,ite)))
print("Expected turns for safe and circle: "+ str(summary(layout,True,0,ite)))
print("Expected turns for normal and no circle: "+ str(summary(layout,False,1,ite)))
print("Expected turns for normal and circle: "+ str(summary(layout,True,1,ite)))
print("Expected turns for risky and no circle: "+ str(summary(layout,False,2,ite)))
print("Expected turns for risky and circle: "+ str(summary(layout,True,2,ite)))
