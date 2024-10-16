from turtle import Screen
import pgzrun
import math as m
from random import randint
import numpy as npy
import shelve

# GarbageGoober = []
# for item in GarbageGoober:
#    del data[item]
# NOTE: Mention performance in design doc

# Global Definitions
SimSpeed = 1

# Class Library
class PlayerObject:
    npy.array([[0,0],[0,0],[0,0]]) # Player Infomation {(PosX (0,0), PosY (0,1)), (VelX (1,0), VelY (1,1)), (Angleθ (2,0), Rotationθ (2,1))}
class Object:
    npy.array([[0,0],[0,0],[0,0]]) # physics object Infomation {(PosX (0,0), PosY (0,1)), (VelX (1,0), VelY (1,1)), (Angleθ (2,0), Rotationθ (2,1))}

# Get resolution from settings
settings = [open("Data\PlayerData.txt","r")] # todo be able to read/write system parameters from file
WIDTH = 1600
HEIGHT = 900

PlayerActor = Actor('kenney_space-shooter-extension/png/sprites/ships/spaceships_001') # type: ignore (supresses warnings)
PlayerProp = PlayerObject # Delcares Player as Physics Object
PlayerActor.pos = (PlayerProp[0,0], PlayerProp[0,1]) # Places Player actor in world


   
# Shelve Example
# d = shelve.open('score.txt')  # here you will save the score variable   
# d['score'] = score            # thats all, now it is saved on disk.
# score = d['score']  # the score is read from disk
# d.close()

def draw():
    PlayerActor.draw()


def update():
    #Create GarbageGoober The Memory Leak Guardian
    GarbageGoober = []

    # Calculate delta_time
    last_time
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    # Update position based on speed and delta time
    delta_PosX = PlayerPropeties * delta_time
    delta_PosY = PlayerPropeties[3] * delta_time

    # Update Velocity based on Accelleration and delta time
    delta_vx = AccX * delta_time
    delta_vy = AccY * delta_time

    # Update Angleθ based on Accelleration and delta time
    delta_Angleθ = PlayerPropeties[5] * delta_time

    # Update Rotation Speed based on Accelleration and delta time
    delta_Rotθ = Accθ * delta_time

    delta_Properties = data[npy.array([[delta_PosX, delta_PosY], [delta_vx, delta_vy], [delta_Angleθ, delta_Rotθ]])]
    PlayerProperties += delta_Properties

    ClearMemory()

def ClearMemory():
    for item in GarbageGoober:
        del data[item]

pgzrun.go()