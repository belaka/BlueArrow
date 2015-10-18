import pygame
import pygame.camera
from time import sleep
import sys

pygame.init()
pygame.camera.init()

mycams = pygame.camera.list_cameras()

if mycams:
    # Assume first camera is the one we want
    mycamera = mycams[0]
else:
    print "No camera found"
    sys.exit(0)

cam = pygame.camera.Camera(mycamera, (300,240))
cam.start()

screen = pygame.display.set_mode((300,240))

camera_quit = False

while not camera_quit:
    for event in pygame.event.get():
       
        # Handle quit message received
        if event.type == pygame.QUIT:
            camera_quit=True
       
        # 'Q' to quit   
        if (event.type == pygame.KEYUP):
            if (event.key == pygame.K_q):
                camera_quit = True
   
    im = pygame.transform.flip(cam.get_image(),True, False)
    screen.blit(im,(0,0))
    pygame.display.flip()
    sleep(0.1)
