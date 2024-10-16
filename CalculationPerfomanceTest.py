import pgzrun
import random
import math as m
import numpy as npy
import os
import time

# Screen
WIDTH = 1600
HEIGHT = 900

# ---- Global Definitions ----
#initialisation and image cache
SimSpeed = 1.00
Gravity = 0.00
accY = 0.00
accX = 0.00
calcCount = 0
calcTime = 0.00

ActorScaleTest = Actor('spaceships_001') # type: ignore (supresses warnings)
ActorScaleTest.angle = 180
ActorScaleTest.scale = 1.00
ActorScaleTest.pos = (WIDTH/2, HEIGHT/2)

PlayerActor = Actor('spaceships_001') # type: ignore (supresses warnings)
PlayerProp = npy.array([[WIDTH/2, HEIGHT/2], [0, 0], [180, 0] ]) # Player Infomation [[(PosX (0,0), PosY (0,1)], [VelX (1,0), VelY (1,1)], [Angleθ (2,0), Angleω (2,1)]]

def update(dt):
    global accY, accX, Gravity, SimSpeed, calcCount, calcTime

    accY = random.randint(-1000,1000)
    accX = random.randint(-1000,1000)
    Gravity += (random.randint(-1,1)/10)
    i=0

    start = time.time()
    while i < 3000:
        # Update VelocityY based on AccY and delta time
        PlayerProp[1,1] = PlayerProp[1,1] + ((accY + Gravity) * (dt*SimSpeed))

        # Update VelocityX based on AccX and delta time
        PlayerProp[1,1] = PlayerProp[1,1] + ((accY + Gravity) * (dt*SimSpeed))
        
        # Update positionY based on speed and delta time
        PlayerProp[0,1] = PlayerProp[0,1] + PlayerProp[1,1] * (dt*SimSpeed)
        PlayerActor.y = PlayerProp[0,1]

        # Update positionX based on speed and delta time
        PlayerProp[0,0] = PlayerProp[0,0] + PlayerProp[1,0] * (dt*SimSpeed)
        PlayerActor.x = PlayerProp[0,1]
        i += 1
        calcCount += 1 

    stop = time.time()
    calcTime = stop-start
    del stop, start
    

def draw():
    screen.fill((20,20,40)) # type: ignore (supresses warnings)
    screen.draw.text('CalcTime: ' + str(calcTime), (WIDTH/2, 50), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
    screen.draw.text('Calculations: ' + str(calcCount), (WIDTH/2, 100), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
    screen.draw.text('Stable FPS: ' + str(1/calcTime), (WIDTH/2, 150), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
    ActorScaleTest.draw()

os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()