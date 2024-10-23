import pgzrun
from pgzhelper import *
import math as m
#import shelve
import numpy as npy
import os
import json
from pathlib import Path
from random import randint


# GarbageGoober = []
# for item in GarbageGoober:
#    del data[item]
# NOTE: Mention performance in design doc

# ---- Global Definitions ----
#initialisation and image cache
SimSpeed = 1.00
Gravity = 98.1
accY = 0.00
#accX = 0.00
score = 0
GameState = 0

screenFocus = 'player'
'spaceships_001'
'spacestation_032'

HighScorePath = Path.joinpath(Path(os.getcwd()) / Path('Data\HighScores.json'))

#import High Scores
def readScores():
    # Opening JSON file
    with open(HighScorePath) as json_file:
        scores = json.load(json_file)
    return scores
def writeScores(HighScores):
    #Write out Scores to json file
    with open(HighScorePath, "w") as outfile:
        json.dump(HighScores, outfile)

Scores = readScores() #read Scores from .json file
HighScores = {k: v for k, v in sorted(Scores.items(), key=lambda item: item[1])} #Sort scores displaying the Highest first

print(HighScores)

# Class Library
#class DynamicObject:
    #npy.array([ [0, 0], [0, 0], [0, 0] ]) # Object Infomation [[(PosX (0,0), PosY (0,1)], [VelX (1,0), VelY (1,1)], [Angleθ (2,0), Angleω (2,1)]]
    #mass = 0
    #inView = False
#class StaticObject:
    #npy.array([0, 0, 0]) #Center of Mass Information [PosX (0), PosY (1), Angleθ(2)]
    #mass = 0
    #inView = False

# Screen
WIDTH = 1600
HEIGHT = 900

# PlayerActor
PlayerActor = Actor('spaceships_001') # type: ignore (supresses warnings)
#PlayerProp = DynamicObject # Player Infomation [[(PosX (0,0), PosY (0,1)], [VelX (1,0), VelY (1,1)], [Angleθ (2,0), Angleω (2,1)]]
#PlayerProp = [[WIDTH/2, 0], [0, 0], [180, 0] ] # Initialise player properties
#PlayerProp.inView = True 
PlayerProp = npy.array([0.00, 0.00]) # Initialise 1-d player properties (PosY (0), VelY (1))
PlayerActor.angle = 180


#Terrain
LandingPad = Actor('spacestation_032') 
#LandingPadProp = StaticObject
LandingPad.pos = WIDTH/2, HEIGHT-100
    
# User Inputs
def UserInputs():
    global PlayerProp, accY, GameState, score
    if keyboard.space: # type: ignore (supresses warnings)
        if GameState == 3:
            writeScores(HighScores)
            GameState = 1
        if GameState == 0:
            GameState = 1
        if accY > -1500.00:
            accY -= 10.00 #throttle up of 10 appears to be good
    #elif accY < 0:
        #accY += 50 #throttle down of 50 makes the down throttle snappy but not so much it can't be toggled
    else:
        accY = 0
    if keyboard.r: # type: ignore (supresses warnings)
        if GameState == 2:
            PlayerProp = npy.array([0.00,0.00]) #Reset Player Properties
            GameState = 1
            score = 0
    if keyboard.h: # type: ignore (supresses warnings)
        if GameState == 2:
            GameState = 3
        


def CheckCollision():
    global PlayerProp, GameState, PlayerActor, LandingPad, score
        #hit = PlayerActor.obb_collidepoints(LandingPad)
    #if hit != -1:
        #if PlayerProp[1] < 10.00:
            #print("you win!")
        #elif PlayerProp[1] >= 10.00:
            #print("you Unalived :(")
    if PlayerActor.colliderect(LandingPad):
        if PlayerProp[1] < 90.00 and PlayerProp[1] >= 0 and GameState == 1:
            score += 1
            PlayerProp = [0-randint(-350,0), randint(-150,300)]
        elif PlayerProp[1] >= 90.00:
            GameState = 2
            PlayerActor.pos = WIDTH/2, 0 # teleport player to start position on fail

#update Function
def update(dt): #update(dt) allows pgz to automatically pass dt into the function
    #using globals
    global accY, Gravity, SimSpeed, PlayerProp, GameState

    UserInputs() #check user inputs

    if (GameState == 1):
        # for (DynamicObj in ) #Update Dynamic objects in view
        # Update VelocityY based on AccY and delta time
        #PlayerProp[1,1] = PlayerProp[1,1] + ((accY + Gravity) * (dt*SimSpeed))
        PlayerProp[1] = PlayerProp[1] + ((accY + Gravity) * (dt*SimSpeed))
        
        # Update positionY based on speed and delta time
        #PlayerProp[0,0] = PlayerProp[0,0] + PlayerProp[1,0] * (dt*SimSpeed)
        PlayerProp[0] = PlayerProp[0] + PlayerProp[1] * (dt*SimSpeed)
        #PlayerActor.y = PlayerProp[0]

        # Update positionY based on speed and delta time
        #PlayerProp[0,0] = PlayerProp[0,0] + PlayerProp[1,0] * (dt*SimSpeed)
        #PlayerActor.x = WIDTH/2

        #animate player
        animate(PlayerActor, pos=(WIDTH/2,PlayerProp[0]), tween='linear', duration=dt) #type: ignore
    
    CheckCollision()

def draw():
    global score
    screen.fill((20,20,40)) # type: ignore (supresses warnings)
    if GameState == 0:
        screen.draw.text('DARK FRONTIER V0.1', center=(WIDTH/2, HEIGHT/2-50), color=(255,15,15), fontsize=120) # type: ignore (supresses warnings)
        screen.draw.text('Press Space to start', center=(WIDTH/2, HEIGHT/2+50), color=(255,255,255), fontsize=40) # type: ignore (supresses warnings)
    if GameState == 1:
        PlayerActor.draw()
        LandingPad.draw()
        screen.draw.text('Score: ' + str(score), (15,10), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
        screen.draw.text('Thrust: ' + str(accY), (15, 60), color=(255,255,255), fontsize=30)# type: ignore (supresses warnings) 
        screen.draw.text('Speed: ' + str("{:.2f}".format(PlayerProp[1])), (15, 90), color=(255,255,255), fontsize=30) # type: ignore (supresses warnings)
        screen.draw.text('Height: ' + str("{:.2f}".format(-PlayerProp[0]/10+80)), (15, 120), color=(255,255,255), fontsize=30) # type: ignore (supresses warnings)
    if GameState == 2:
        screen.draw.text('Game Over', center=(WIDTH/2, HEIGHT/2-50), color=(255,0,0), fontsize=120) # type: ignore (supresses warnings)
        screen.draw.text('Final Score: ' + str(score), center=(WIDTH/2, HEIGHT/2+50), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
        screen.draw.text('Press R to Restart, Press H to Save Highschore', center=(WIDTH/2, HEIGHT*(4/5)), color=(255,255,255), fontsize=30) # type: ignore (supresses warnings)
    if GameState == 3:
        screen.draw.text('Highscores:', center=(WIDTH/2, HEIGHT/5), color=(255,255,255), fontsize=90) # type: ignore (supresses warnings)
 
os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()