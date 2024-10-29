import pgzrun
from pgzhelper import *
import math as m
#import shelve
import numpy as npy
import os
import json
from pathlib import Path
from random import randint

#File Paths
highscorePath = Path.joinpath(Path(os.getcwd()) / Path('Data\HighScores.json'))

#Read/Write JSON Methods
def ReadJSON(path):
    # Opening JSON file
    with open(path) as json_file:
        return json.load(json_file)
    return scores
def WriteJSON(content, path): #Write Method (bool amend?, string/dict content, path to JSON file)
    #Write out Scores to json file
    with open(path, "w") as outfile:
        json.dump(content, outfile)
def SortDict(dictionary, reversed):
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=reversed)}

#read Scores from .json file
Scores = ReadJSON(highscorePath) 
print('File: ', Scores)

#Sort scores displaying the Highest first
HighScores = SortDict(Scores, True) 
print('Sorted: ', HighScores)

#Write Highscores to File
WriteJSON(HighScores, highscorePath) 

#Dict examples
#add OR append if exists
HighScores['TestScore'] = 35 
print('amended score: ', HighScores)
#Increment
HighScores['TestScore'] += 1 
print('Incremented TestScore: ', HighScores)
# Convert dictionary values to a list
values_list = list(HighScores.values())  
print('Values List: ', values_list)
#Returns list of keys, highest value to lowest
SortedKeyList = sorted(Scores, key=Scores.get, reverse=True) 
print('Sorted Key List: ', SortedKeyList)

WriteJSON(HighScores, highscorePath)