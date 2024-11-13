import pgzrun
from pgzhelper import *
#import math as m
#import shelve
import numpy as npy
import os
import json
from pathlib import Path
from random import randint

#Todo: Add Background
#Todo: Add Thrust Animation

pygame.init()
# GarbageGoober = []
# for item in GarbageGoober:
#    del data[item]
# NOTE: Mention performance in design doc

#region ---- Global Definitions ----
#initialisation and image cache
SimSpeed: float = 1.00
Gravity: float = 98.1
Fuel: int = 500
accY: float = 0.00
#accX: float = 0.00
score: int = 0
PlayerSpeed: int = 0
GameState: bytes = 0 #0: Title Screen, 1: Game, 2: Game Over, 3: Highscores, 4: Add Highscore
screenFocus: bytes = 0 #0: unbound, 1: player, 2: other
name: str = ""
#endregion

#region ---- Cache ----
#images
'spaceships_001', 'spacestation_032'
#endregion

#region ---- File Paths ----
highscorePath:Path = Path.joinpath(Path(os.getcwd()) / Path('Data\HighScores.json'))
#endregion

#region ---- Methods ----
#Read/Write JSON Methods
def ReadJSON(path):
    with open(path) as json_file: # Opening JSON file
        return json.load(json_file)
    return scores
def WriteJSON(content, path): #Write Method (Dictionary content, path to JSON file)
    #Write out Scores to json file
    with open(path, "w") as outfile:
        json.dump(content, outfile)
def SortDict(dictionary, reversed):
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=reversed)}

#Colision Method
def CheckCollision():
    global PlayerProp, GameState, PlayerActor, LandingPad, score, Fuel
        #hit = PlayerActor.obb_collidepoints(LandingPad)
    #if hit != -1:
        #if PlayerProp[1] < 10.00:
            #print("you win!")
        #elif PlayerProp[1] >= 10.00:
            #print("you Unalived :(")
    if PlayerActor.colliderect(LandingPad):
        if PlayerProp[1] < 90.00 and PlayerProp[1] > 0 and GameState == 1:
            sounds.lowfrequency_explosion_001.play()# type: ignore (supresses warnings)
            #PlayerActor.pos = WIDTH/2, 100
            PlayerProp = [0-randint(-350,0), randint(-150,300)]
            score += 1
            Fuel += randint(100,150)
            #print("you win!")
        elif PlayerProp[1] > 90.00: 
            sounds.thrusterfire_003.stop() # type: ignore (supresses warnings)
            sounds.explosioncrunch_000.play() # type: ignore (supresses warnings)
            GameState = 2
            #print("you Unalived :(")


#display Highscore
def CreateScoreboard(scores: dict):
    scoreboardstring = ''
    i = 1
    for k, v in scores.items():
        if i <= 10:
            scoreboardstring += str(i) + ': ' + k + ': ' + str(v) + '\n'
            i += 1
    return scoreboardstring

def ResetGame():
    global PlayerActor, PlayerProp, score, Fuel
    PlayerActor.pos = WIDTH/2, -100
    PlayerProp = npy.array([-100.00, 0.00])
    score = 0
    Fuel = 500
    
#endregion

HighScores = ReadJSON(highscorePath) #read Scores from .json file

#region ---- Class Library ----
#class DynamicObject:
    #npy.array([ [0, 0], [0, 0], [0, 0] ]) # Object Infomation [[(PosX (0,0), PosY (0,1)], [VelX (1,0), VelY (1,1)], [Angleθ (2,0), Angleω (2,1)]]
    #mass = 0
    #inView = False
#class StaticObject:
    #npy.array([0, 0, 0]) #Center of Mass Information [PosX (0), PosY (1), Angleθ(2)]
    #mass = 0
    #inView = False
#endregion

#region ---- Screen ----
WIDTH = 1600
HEIGHT = 900
pgzrun.os.environ['SDL_VIDEO_CENTERED'] = '1'
#endregion

#region ---- PlayerActor ----
PlayerActor = Actor('spaceships_001') # type: ignore (supresses warnings)
#PlayerProp = DynamicObject # Player Infomation [[(PosX (0,0), PosY (0,1)], [VelX (1,0), VelY (1,1)], [Angleθ (2,0), Angleω (2,1)]]
#PlayerProp = [[WIDTH/2, 0], [0, 0], [180, 0] ] # Initialise player properties
#PlayerProp.inView = True 
PlayerProp = npy.array([0.00, 0.00]) # Initialise 1-d player properties (PosY (0), VelY (1))
#endregion

#region ---- Terrain ----
LandingPad = Actor('spacestation_032') 
#LandingPadProp = StaticObject
LandingPad.pos = WIDTH/2, HEIGHT-100
#endregion

#region ---- Sounds ----

#endregion


#region ---- User Inputs ----
def UserInputs():
    global PlayerProp, accY, GameState, score, Fuel
    if GameState == 0:
        if keyboard.SPACE: # type: ignore (supresses warnings)
            GameState = 1
    if GameState == 1:
        if keyboard.SPACE: # type: ignore (supresses warnings)
            if Fuel > 0 and accY > -1500.00:
                accY -= 10.00 #throttle up of 10 appears to be good
                Fuel -= 1
        elif accY < 0:
            accY += 50 #throttle down of 50 makes the down throttle snappy but not so much it can't be toggled
        else:
            sounds.thrusterfire_003.stop() # type: ignore (supresses warnings)
            accY = 0
    if GameState == 2:
        if keyboard.R: # type: ignore (supresses warnings)
            ResetGame()
            GameState = 1  
        if keyboard.H: # type: ignore (supresses warnings)
            GameState = 3
    if GameState == 3:
        if keyboard.R: # type: ignore (supresses warnings)
            ResetGame()
            GameState = 1 
        if keyboard.SPACE: # type: ignore (supresses warnings)
            GameState = 4
    if GameState == 4:
        if keyboard.RETURN: # type: ignore (supresses warnings)
            if HighScores[str(name)] > score: #Todo: prevent overriting of higher scores
                HighScores[name + ' copy'] = score
                HighScores = SortDict(HighScores,True)
            else:
                HighScores[str(name)] = score
                HighScores = SortDict(HighScores,True)
            WriteJSON(HighScores, highscorePath)
            GameState = 3
        if keyboard.ESCAPE: # type: ignore (supresses warnings)
            GameState = 3
            

def on_key_down(key, mod, unicode):
    global name, GameState, HighScores,highscorePath
    if GameState == 1:
        if (key == pygame.K_SPACE):
            sounds.thrusterfire_003.play(-1) # type: ignore (supresses warnings)
    if GameState == 4:
        if key != pygame.K_BACKSPACE and key != pygame.K_RETURN and key != pygame.K_ESCAPE:
            name += unicode
        elif key == pygame.K_BACKSPACE:
            name = name[:-1]
        elif key == pygame.K_BACKSPACE:
            GameState = 3
        elif key == pygame.K_RETURN: # type: ignore (supresses warnings)
            #if HighScores[name] > score:
                #HighScores[name+'copy'] = score
                #HighScores = SortDict(HighScores,True)
            #else:
            HighScores[name] = score
            HighScores = SortDict(HighScores,True)
            WriteJSON(HighScores, highscorePath)
            GameState = 3
#endregion
        
#region ---- Update Function ----
def update(dt): #update(dt) allows pgz to automatically pass dt into the function
    #using globals
    global accY, Gravity, SimSpeed, PlayerProp, GameState, PlayerSpeed

    UserInputs() #check user inputs

    if (GameState == 1):
        CheckCollision()
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
        #if (accY !=0):
            #if accY < 250

        # update absolute player speed
        if (PlayerProp[1]<0):
            PlayerSpeed = PlayerProp[1] * -1
        else:
            PlayerSpeed = PlayerProp[1]
    
    
#endregion

#region ---- Draw Function ----
def draw():
    global HighScores, score, Fuel, accY, name, GameState, PlayerSpeed
    screen.fill((20,20,40)) # Background, #type: ignore (supresses warnings)
    if GameState == 0:
        screen.draw.text('DARK FRONTIER V0.1', center=(WIDTH/2, HEIGHT/2-50), color=(255,15,15), fontsize=120) # type: ignore (supresses warnings)
        screen.draw.text('Press Space to start', center=(WIDTH/2, HEIGHT/2+50), color=(255,255,255), fontsize=40) # type: ignore (supresses warnings)
    if GameState == 1:
        PlayerActor.draw()
        LandingPad.draw()
        screen.draw.text('Score: ' + str(score), (15,10), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
        screen.draw.text('Thrust: ' + str(-accY), (15, 60), color=(255,255,255), fontsize=30)# type: ignore (supresses warnings) 
        screen.draw.text('Speed: ' + str("{:.2f}".format(PlayerSpeed)), (15, 90), color=(255,255,255), fontsize=30) # type: ignore (supresses warnings)
        screen.draw.text('Height: ' + str("{:.2f}".format(-PlayerProp[0]/10+80)), (15, 120), color=(255,255,255), fontsize=30) # type: ignore (supresses warnings)
        screen.draw.text('Fuel: ' + str(Fuel), (15, 150), color=(255,255,255), fontsize=30) # type: ignore (supresses warnings)
    if GameState == 2:
        screen.draw.text('Game Over', center=(WIDTH/2, HEIGHT/2-50), color=(255,0,0), fontsize=120) # type: ignore (supresses warnings)
        screen.draw.text('Final Score: ' + str(score), center=(WIDTH/2, HEIGHT/2+50), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
        screen.draw.text('Press R to Restart, Press H to Show Highscores', center=(WIDTH/2, HEIGHT*(4/5)), color=(255,255,255), fontsize=30) # type: ignore (supresses warnings)
    if GameState == 3:
        HighScores = SortDict(HighScores,True)
        ScoreBoardString = CreateScoreboard(HighScores)
        scoreBox = Rect((WIDTH/5, HEIGHT/5), (3*WIDTH/5, 3*HEIGHT/5)) 
        screen.draw.text('Highscores:', center=(WIDTH/2, HEIGHT/6), color=(255,15,15), fontsize=90) # type: ignore (supresses warnings)
        screen.draw.textbox(ScoreBoardString, scoreBox, color=(255,255,255)) # type: ignore (supresses warnings)
        # screen.draw.text(, midtop=(WIDTH/2, HEIGHT/5+50), color=(255,255,255), fontsize=90) # type: ignore (supresses warnings)
        screen.draw.text('Your Score: ' + str(score), (15,10), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
        screen.draw.text('Press R to Restart, Press SPACE to Save Your Score', center=(WIDTH/2, HEIGHT*(4/5)), color=(255,255,255), fontsize=30) # type: ignore (supresses warnings)
    if GameState == 4: # To Do: Add rect For Scoreboard
        screen.draw.text('Enter Your Name:', center=(WIDTH/2, HEIGHT/2-50), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
        screen.draw.text(str(name), center=(WIDTH/2, HEIGHT/2), color=(255,255,255), fontsize=90) # type: ignore (supresses warnings)
        screen.draw.text('Score: ' + str(score), center=(WIDTH/2, HEIGHT/2+50), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
        screen.draw.text('Press ESC to Exit, Press ENTER to Save', center=(WIDTH/2, HEIGHT*(4/5)), color=(255,255,255), fontsize=30) # type: ignore (supresses warnings)screen.draw.text('Press R to Restart, Press H to Save Your Score', center=(WIDTH/2, HEIGHT*(4/5)), color=(255,255,255), fontsize=30) # type: ignore (supresses warnings)
#endregion
 
pgzrun.go()