import pgzrun
from pgzhelper import *
import math as m
import numpy as npy
import os


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
game_over = False
'spaceships_001'
'spacestation_032'

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
    

#update Function
def update(dt): #update(dt) allows pgz to automatically pass dt into the function
    #using globals
    global accY, Gravity, SimSpeed, PlayerProp, score, game_over

    # User Inputs
    if keyboard.space: # type: ignore (supresses warnings)
        if accY > -500.00:
            accY -= 5.00
    elif accY < 0:
        accY += 8
    else:
        accY = 0
        
    # for (DynamicObj in ) #Update Dynamic objects in view
    # Update VelocityY based on AccY and delta time
    #PlayerProp[1,1] = PlayerProp[1,1] + ((accY + Gravity) * (dt*SimSpeed))
    PlayerProp[1] = PlayerProp[1] + ((accY + Gravity) * (dt*SimSpeed))
    
    # Update positionY based on speed and delta time
    #PlayerProp[0,0] = PlayerProp[0,0] + PlayerProp[1,0] * (dt*SimSpeed)
    PlayerProp[0] = PlayerProp[0] + PlayerProp[1] * (dt*SimSpeed)
    PlayerActor.y = PlayerProp[0]

    # Update positionY based on speed and delta time
    #PlayerProp[0,0] = PlayerProp[0,0] + PlayerProp[1,0] * (dt*SimSpeed)
    PlayerActor.x = WIDTH/2
    
    

    #hit = PlayerActor.obb_collidepoints(LandingPad)
    #if hit != -1:
        #if PlayerProp[1] < 10.00:
            #print("you win!")
        #elif PlayerProp[1] >= 10.00:
            #print("you Unalived :(")
    if PlayerActor.colliderect(LandingPad):
        if PlayerProp[1] < 40.00:
            score += 1
            PlayerProp = [0, 10]
        elif PlayerProp[1] >= 40.00:
            game_over = True


def draw():
    global score
    screen.fill((20,20,40)) # type: ignore (supresses warnings)
    PlayerActor.draw()
    LandingPad.draw()
    screen.draw.text('Score: ' + str(score), (15,10), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
    screen.draw.text('Thrust: ' + str(accY), (15, 60), color=(255,255,255), fontsize=30)# type: ignore (supresses warnings) 
    screen.draw.text('Speed: ' + str("{:.2f}".format(PlayerProp[1])), (15, 90), color=(255,255,255), fontsize=30) # type: ignore (supresses warnings)
    screen.draw.text('Height: ' + str("{:.2f}".format(-PlayerProp[0]/10+80)), (15, 120), color=(255,255,255), fontsize=30) # type: ignore (supresses warnings)
    if game_over:
        screen.draw.text('Game Over', (WIDTH/2, HEIGHT/2-50), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
        screen.draw.text('Final Score: ' + str(score), (WIDTH/2, HEIGHT/2+50), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
 
os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()