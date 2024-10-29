import pgzrun
from pgzhelper import *
import math as m
import numpy as npy
import os

# Screen
WIDTH = 1600
HEIGHT = 900

ActorScaleTest = Actor('spaceships_001') # type: ignore (supresses warnings)
ActorScaleTest.angle = 180
ActorScaleTest.scale = 1.00
ActorScaleTest.pos = (WIDTH/2, HEIGHT/2)

def update():
    if keyboard.up: # type: ignore (supresses warnings)
        ActorScaleTest.scale += 0.01
    if keyboard.down: # type: ignore (supresses warnings)
        ActorScaleTest.scale -= 0.01

def draw():
    screen.fill((20,20,40)) # type: ignore (supresses warnings)
    screen.draw.text('Scale: ' + str("{:.2f}".format(ActorScaleTest.scale)), (WIDTH/2, 100), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
    ActorScaleTest.draw()

os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()