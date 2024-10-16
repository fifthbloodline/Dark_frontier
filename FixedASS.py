import pygame
pygame.init()
from pygame.locals import *

from random import randint
import math as m

# Planet Types:
# 0 - Solid Planet
# 1 - Gas Planet
# 2 - Small Star
# 3 - Big Star
# 4 - Black Hole

data = {
    "sun": {
        "col": (255, 255, 0),
        "rad": 35,
        "grav": 30,
        "pos": [800, 450],
        "vel": [0, 0],
        "type": 3
    },
    "earth": {
        "col": (100, 100, 255),
        "rad": 4,
        "grav": .01,
        "pos": [1100, 450],
        "vel": [0, -8],
        "type": 0
    },
    "venus": {
        "col": (255, 50, 50),
        "rad": 3,
        "grav": 0.09,
        "pos": [1000, 450],
        "vel": [0, -6],
        "type": 0
    },
    "mars": {
        "col": (255, 0, 0),
        "rad": 2,
        "grav": 0.04,
        "pos": [1200, 450],
        "vel": [0, -10],
        "type": 0
    },
    "jupiter": {
        "col": (255, 150, 150),
        "rad": 8,
        "grav": .24,
        "pos": [300, 450],
        "vel": [0, 10],
        "type": 1
    }
}

winSize = (1600, 900)
display = pygame.display.set_mode(winSize)
fps = 54
clock = pygame.time.Clock()

simSpeed = 0.01

def collision_outcome(type1, type2):
    if type1 == 0:
        if type2 == 0 or type2 == 1: return 0
    if type1 == 1:
        if type2 == 0 or type2 == 1: return 1
    if type1 == 2:
        if type2 == 0: return 2
        if type2 == 1 or type2 == 2: return 3
    if type1 == 3:
        if type2 == 0 or type2 == 1: return 3
        if type2 == 2 or type2 == 3: return 4

stars = [((randint(150, 200), randint(150, 200), randint(150, 200)), (randint(1, winSize[0]), randint(1, winSize[1])), randint(1, 2)) for _ in range(250)]
def draw_stars():
    for star in stars:
        pygame.draw.circle(display, star[0], star[1], star[2])

def draw_planets():
    for planet in data:
        pygame.draw.circle(display, data[planet]['col'], data[planet]['pos'], data[planet]['rad'])

def update_planets():
    toDelete = []
    for planet in data:
        for oPlanet in data:
            if oPlanet != planet:
                dx = data[oPlanet]['pos'][0] - data[planet]['pos'][0]
                dy = data[oPlanet]['pos'][1] - data[planet]['pos'][1]

                distance = m.sqrt(dx*dx + dy*dy)

                delta_vx = (dx / distance) * data[oPlanet]['grav'] * simSpeed / ((data[planet]['grav']+1)**3)
                delta_vy = (dy / distance) * data[oPlanet]['grav']* simSpeed / ((data[planet]['grav']+1)**3)

                data[planet]['vel'][0] += delta_vx
                data[planet]['vel'][1] += delta_vy

                if distance <= data[oPlanet]['rad']:
                    toDelete.append(planet)
                    data[oPlanet]['grav'] += data[planet]['grav']
                    data[oPlanet]['rad'] += data[planet]['rad'] / 2
                    co = collision_outcome(data[oPlanet]['type'], data[planet]['type'])
                    if co == 0: data[oPlanet]['col'] = (150, 0, 0)
                    elif co == 1: data[oPlanet]['col'] = (255, 150, 150)
                    elif co == 2: data[oPlanet]['col'] = (255, 255, 0)
                    elif co == 3: data[oPlanet]['col'] = (255, 0, 0)
                    elif co == 4:
                        data[oPlanet]['col'] = (20, 20, 20)
                        data[oPlanet]['grav'] *= 2
                    data[oPlanet]['type'] = co

        data[planet]['pos'][0] += data[planet]['vel'][0]
        data[planet]['pos'][1] += data[planet]['vel'][1]

    for item in toDelete:
        del data[item]

run = True
while run:
    display.fill((0, 0, 0))

    draw_stars()
    draw_planets()
    update_planets()

    clock.tick(fps)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

pygame.quit()