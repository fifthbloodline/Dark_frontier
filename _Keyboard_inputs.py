import pgzrun
from pgzhelper import *
import os

# Screen
WIDTH = 1600
HEIGHT = 900

ActorScaleTest = Actor('spaceships_001') # type: ignore (supresses warnings)
ActorScaleTest.angle = 180
ActorScaleTest.scale = 1.00
ActorScaleTest.pos = (WIDTH/2, HEIGHT/2)
user_text = ''

def on_key_down(key, mod, unicode):
    print("key ", unicode, "pressed.")


def update():
    global user_text # type: ignore (supresses warnings)
    event = pygame.event.get()
        #if event.type == pygame.K_BACKSPACE:
            #user_text = user_text[:-1]
        #else:
    user_text = event
    
       
    
    

def draw():
    screen.fill((20,20,40)) # type: ignore (supresses warnings)
    screen.draw.text('Pressed Keys: ' + str(user_text), center=(WIDTH/2, 100), color=(255,255,255), fontsize=60) # type: ignore (supresses warnings)
    ActorScaleTest.draw()

pgzrun.os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()