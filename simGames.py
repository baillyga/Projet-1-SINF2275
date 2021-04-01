# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 18:49:02 2021

@author: Corentin ZONE
         Gabriel BAILLY
         Lara WAUTIER
"""

import random
import itertools
import pandas as pd

import numpy as np


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
    empircalcost=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    while pos<14:
        for i in range(0,14):
            if empircalcost[i]!=0:
                empircalcost[i]+=1

        if empircalcost[pos]==0:
            empircalcost[pos]+=1

        turn += 1
        #selection of the strategy for the game
        if strategy[pos]==0:
            dice_roll=(0,security_dice())
        elif strategy[pos]==1:
            dice_roll=(1,normal_dice())
        elif strategy[pos]==2:
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
    return [out,empircalcost]

layout=[0,1,0,0,3,0,4,2,0,0,4,2,0,0]
#layout=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
strat0=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
strat1=[1,1,1,1,1,1,1,1,1,1,1,1,1,1]
strat2=[2,2,2,2,2,2,2,2,2,2,2,2,2,2]
strat3=np.random.randint(0,3,14)
result=game(layout,True,strat3)[0]
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
        result=game(layout,circle,strategy)[0]
        total_turn+=result[len(result)-1][5]
        stop+=1
    return total_turn/iteration

ite=1000000
print("Expected turns for random and no circle: "+ str(summary(layout,False,strat3,ite)))
print("Expected turns for random and circle: "+ str(summary(layout,True,strat3,ite)))
print("Expected turns for safe and no circle: "+ str(summary(layout,False,strat0,ite)))
print("Expected turns for safe and circle: "+ str(summary(layout,True,strat0,ite)))
print("Expected turns for normal and no circle: "+ str(summary(layout,False,strat1,ite)))
print("Expected turns for normal and circle: "+ str(summary(layout,True,strat1,ite)))
print("Expected turns for risky and no circle: "+ str(summary(layout,False,strat2,ite)))
print("Expected turns for risky and circle: "+ str(summary(layout,True,strat2,ite)))


def empirical(layout,circle,strat,iteration):
    stop = 0
    total_turn = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    result=[]
    while stop < iteration:
        result.append(game(layout, circle, strat)[1])
        stop += 1
    a=0
    for i in range(0,14):
        for y in result:
            if y[i]!=0:
                total_turn[i]+=y[i]
                a+=1
        total_turn[i]=total_turn[i]/a
        a=0
    return total_turn

layout=[0,1,0,0,3,0,4,2,0,0,4,2,0,0]
optStrat=[2,1,2,2,1,2,2,2,1,0,2,0,1,0]
print("empirical number of turn for each squares (cirlce): "+ str(empirical(layout,True,optStrat,1000)))

optStrat=[2,1,2,2,1,2,2,2,2,2,2,0,2,2]
print("empirical number of turn for each squares (no cirlce): "+ str(empirical(layout,False,optStrat,1000)))

result=game(layout,False,optStrat)[0]
table="Dice   Value   position   trap  triggered  nb_turn"
for i in range(0,len(result)):
    table+="\n{:^5}  {:^5}     {:^5}   {:^5}    {:^5}    {:^5} ".format(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],result[i][5])
print(table)

layout=[0,1,0,2,3,0,2,0,1,0,4,2,0,4]
optStrat=[1,0,2,1,2,1,0,0,0,0,0,0,1,0]
print("empirical number of turn for each squares (cirlce): "+ str(empirical(layout,True,optStrat,1000000)))

optStrat=[1,0,2,1,2,1,0,0,0,2,0,0,2,0]
print("empirical number of turn for each squares (no cirlce): "+ str(empirical(layout,False,optStrat,1000000)))



def distSim(layout,circle,strategy,iteration):
    """
    Inputs:
        - layout : vector of traps on the board
        - circle : if circle rule applies
        - strategy : 0 if only safe, 1 if only normal, 2 if only risky, 3 if random
    --------------------------------------------------------------------------------
    Outputs:
        - vector of length <iteration> (used to represent the distribution)
    """
    stop = 0
    dist = []
    while stop <= iteration-1:
        res = game(layout,circle,strategy)[0]
        dist.append(len(res))
        stop += 1
    return dist

layout = [0,1,0,2,3,0,2,0,1,0,4,2,0,4]

stratFalse = [1,0,2,1,2,1,0,0,0,2,0,0,2,0]

optDist = distSim(layout, False, stratFalse, ite)
safeDist = distSim(layout,False,strat0,ite)
normalDist = distSim(layout,False,strat1,ite)
riskyDist = distSim(layout,False,strat2,ite)
randomDist = distSim(layout,False,strat3,ite)
dfF = pd.DataFrame(data={"Optimal": optDist, "Security": safeDist, "Normal": normalDist, "Risky": riskyDist, "Random": randomDist})
dfF.to_csv('distFalse.csv') 


# performance if circle = True

stratTrue = [1,0,2,1,2,1,0,0,0,0,0,0,1,0]

optDistT = distSim(layout, True, stratTrue, ite)
safeDistT = distSim(layout,True,strat0,ite)
normalDistT = distSim(layout,True,strat1,ite)
riskyDistT = distSim(layout,True,strat2,ite)
randomDistT = distSim(layout,True,strat3,ite)

dfT = pd.DataFrame(data={"Optimal": optDistT, "Security": safeDistT, "Normal": normalDistT, "Risky": riskyDistT, "Random": randomDistT})
dfT.to_csv('distTrue.csv') 

stratHuman = [1,0,2,0,2,0,0,0,0,2,2,0,2,0]

humanDist = distSim(layout, False, stratHuman, ite)
dfH = pd.DataFrame(data={"Human": humanDist})
dfH.to_csv('distHuman.csv') 



