import sys
import os
import pygame
import cv2.cv as cv

camera_index = 0

DEV_MODE = True

if DEV_MODE ==  False:
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

pygame.init()

#create fullscreen display 640x480
screen = pygame.display.set_mode((320, 240),0)

capture = cv.CaptureFromCAM(camera_index)
while not capture:
  print "error opening capture device, correction attempt"

while True:
    frame = cv.QueryFrame(capture)
    if frame is None:
        print "fail with putting in frame"

    else:
        c = cv.WaitKey(100)
        print 'capturing!'
        cv.SaveImage("pictest.png", frame)
        img=pygame.image.load("pictest.png")
        screen.blit(img,(0,0))
        
    pygame.display.update()
    
    # check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            webcam.stop()
            pygame.quit()
            sys.exit()
