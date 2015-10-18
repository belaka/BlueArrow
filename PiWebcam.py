# import the relevant libraries
import time
import os
import pygame
import pygame.camera
from pygame.locals import *

DEV_MODE = False

if DEV_MODE ==  False:
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

sleeptime__in_seconds = 0.1

# this is where one sets how long the script
# sleeps for, between frames.sleeptime__in_seconds = 0.05
# initialise the display window
screen = pygame.display.set_mode([320, 240])
pygame.mouse.set_visible(DEV_MODE)
pygame.init()
pygame.camera.init()
# set up a camera object
cam = pygame.camera.Camera("/dev/video0",(240, 320))
# start the camera
cam.start()

while 1:

    # sleep between every frame
    time.sleep( sleeptime__in_seconds )
    # fetch the camera image
    image = cam.get_image()
    # blank out the screen
    screen.fill([0,0,0])
    # copy the camera image to the screen
    screen.blit( image, ( 0, 0 ) )
    # update the screen to show the latest screen image
    pygame.display.update()
