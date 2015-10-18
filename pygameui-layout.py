#!/usr/bin/python
'''
 pygameui-layout.py
 
 BlueArrow CarPuter project
 @author Vincent Honnorat <@>
'''

'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
'''


import sys 
import pygame
import os
import pygameui as ui
import logging
import signal
import threading
import time
from wifi import *
from pprint import pprint
import subprocess
import cv2.cv as cv

log_format = '%(asctime)-6s: %(name)s - %(levelname)s - %(message)s'
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(log_format))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

camera_index = 0

DEV_MODE = False

if DEV_MODE ==  False:
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


 
LIST_WIDTH = 280
MARGIN = 20
SMALL_MARGIN = 10

BLUE = 26, 0, 255
CREAM = 254, 255, 25
BLACK = 0, 0, 0
WHITE = 255, 255, 255
YELLOW = 255, 255, 0
RED = 255, 0, 0
GREEN = 0, 255, 0

class MainScreen(ui.Scene):

    def __init__(self):
        ui.Scene.__init__(self)

        self.clock = ui.pygame.time.Clock()

        self.menu_button = ui.Button(ui.Rect(MARGIN, 140, 280, 30), 'Menu')
        self.menu_button.on_clicked.connect(self.main_action)
        self.add_child(self.menu_button)
        
        self.quit_button = ui.Button(ui.Rect(MARGIN, 180, 280, 30), 'Quit')
        self.quit_button.on_clicked.connect(self.main_action)
        self.add_child(self.quit_button)

    def main_action(self, btn, mbtn):
        logger.info(mbtn)
        if btn.text == 'Menu':
            logger.info('Menu was clicked!')
            ui.scene.push(MenuScreen())
        elif btn.text == 'Quit':
            sys.exit()
            
    def display_fps(self, clock):
        ui.pygame.display.flip()

    def update(self, dt):
        #Write function here
        self.clock.tick(0)
        self.clock_button = ui.Button(ui.Rect(MARGIN, MARGIN, 280, 110), str(time.strftime("%Y-%m-%d %H:%M:%S")))
        self.clock_button.on_clicked.connect(self.main_action)
        self.add_child(self.clock_button)
        #Scene Update
        ui.Scene.update(self, dt)


class MenuScreen(ui.Scene):

    def __init__(self):
        ui.Scene.__init__(self)
 
        self.system_button = ui.Button(ui.Rect(MARGIN, MARGIN, 130, 60), 'System')
        self.system_button.on_clicked.connect(self.menu_actions)
        self.add_child(self.system_button)
 
        self.vehicle_button = ui.Button(ui.Rect(170, MARGIN, 130, 60), 'Vehicle')
        self.add_child(self.vehicle_button)
 
        self.media_button = ui.Button(ui.Rect(MARGIN, 100, 130, 60), 'Media')
        self.media_button.on_clicked.connect(self.menu_actions)
        self.add_child(self.media_button)
 
        self.wifi_button = ui.Button(ui.Rect(170, 100, 130, 60), 'Wifi')
        self.wifi_button.on_clicked.connect(self.menu_actions)
        self.add_child(self.wifi_button)
        
        self.quit_button = ui.Button(ui.Rect(MARGIN, 180, 280, 30), 'Quit')
        self.quit_button.on_clicked.connect(self.menu_actions)
        self.add_child(self.quit_button)
        
    def menu_actions(self, btn, mbtn):
        logger.info(btn.text)
         
        if btn.text == 'System':
            logger.info('system was clicked!!!')
            ui.scene.push(SystemScreen())
        elif btn.text == 'Vehicle':
            ui.scene.push(VehicleScreen())
        elif btn.text == 'Media':
            ui.scene.push(MediaScreen())
        elif btn.text == 'Wifi':
            ui.scene.push(WifiScreen())
        elif btn.text == 'Quit':
            sys.exit()

    def update(self, dt):
        ui.Scene.update(self, dt)
        
class SystemScreen(ui.Scene):
    def __init__(self):
        ui.Scene.__init__(self)
 
        self.color_button = ui.Button(ui.Rect(MARGIN, MARGIN, 130, 60), 'Color') 
        self.add_child(self.color_button)
 
        self.time_button = ui.Button(ui.Rect(170, MARGIN, 130, 60), 'Time')
        self.add_child(self.time_button)
 
        self.levels_button = ui.Button(ui.Rect(MARGIN, 100, 130, 60), 'Levels')
        self.add_child(self.levels_button)
 
        self.gauges_button = ui.Button(ui.Rect(170, 100, 130, 60), 'Gauges')
        self.add_child(self.gauges_button)
        
        self.back_button = ui.Button(ui.Rect(MARGIN, 180, 280, 30), 'Back')
        self.back_button.on_clicked.connect(self.system_actions)
        self.add_child(self.back_button)

    def system_actions(self, btn, mbtn):
        logger.info(btn.text)
         
        if btn.text == 'Back':
            logger.info('back was clicked!!!')
            ui.scene.push(MenuScreen())
        elif btn.text == 'Color':
            ui.scene.push(ColorScreen())
        elif btn.text == 'Time':
            ui.scene.push(TimeScreen())
        elif btn.text == 'Levels':
            ui.scene.push(LevelsScreen())
        elif btn.text == 'Gauges':
            ui.scene.push(GaugesScreen())
            
    def update(self, dt):
        ui.Scene.update(self, dt)
        
class WifiScreen(ui.Scene):
    def __init__(self):
        ui.Scene.__init__(self)
        
        self.connect_button = ui.Button(ui.Rect(MARGIN, 140, 130, 30), 'Connect')
        self.connect_button.on_clicked.connect(self.wifi_actions)
        self.add_child(self.connect_button)
        
        self.refresh_button = ui.Button(ui.Rect(170, 140, 130, 30), 'Refresh')
        self.refresh_button.on_clicked.connect(self.wifi_actions)
        self.add_child(self.refresh_button)
        
        self.back_button = ui.Button(ui.Rect(MARGIN, 180, 280, 30), 'Back')
        self.back_button.on_clicked.connect(self.wifi_actions)
        self.add_child(self.back_button)
        
        scrollbar_size = ui.SCROLLBAR_SIZE
        
        list_of_open = []
        list_of_open = self.check_open_ssids()
        time.sleep(3)
        
        # 2). If we find open ssids turn light and buzzer on, print to SSID.
        labels = [ui.Label(ui.Rect(MARGIN, 180, 260, 30), item, halign=ui.LEFT) for item in list_of_open]
        list_view = ui.ListView(ui.Rect(0, 0, 260, 80), labels)
        list_view.on_selected.connect(self.item_selected)
        list_view.on_deselected.connect(self.item_deselected)
        self.scroll_list = ui.ScrollView(ui.Rect(MARGIN, MARGIN, 260, 80), list_view)
        self.add_child(self.scroll_list)
            
    def item_selected(self, list_view, item, index):
        item.state = 'selected'

    def item_deselected(self, list_view, item, index):
        item.state = 'normal'
            
    def check_open_ssids(self):
        open_ssids = ["--SELECT AN SSID--"]
        for cell in Cell.all('wlan0'):
            #if cell.encrypted == False:
                # print cell.ssid
            open_ssids.append(cell.ssid)
        return open_ssids

    def wifi_actions(self, btn, mbtn):
        logger.info(btn.text+' was clicked!!!') 
        
        if btn.text == 'Back':
            ui.scene.push(MenuScreen())
        elif btn.text == 'Connect':
            ui.scene.push(MenuScreen())
        elif btn.text == 'Refresh':
            ui.scene.push(MenuScreen())
            
            
    def update(self, dt):
        ui.Scene.update(self, dt)

class MediaScreen(ui.Scene):

    def __init__(self):
        ui.Scene.__init__(self)
 
        self.radio_button = ui.Button(ui.Rect(MARGIN, MARGIN, 130, 60), 'Radio')
        self.radio_button.on_clicked.connect(self.media_actions)
        self.add_child(self.radio_button)
 
        self.social_button = ui.Button(ui.Rect(170, MARGIN, 130, 60), 'Social')
        self.social_button.on_clicked.connect(self.media_actions)
        self.add_child(self.social_button)
 
        self.broadcast_button = ui.Button(ui.Rect(MARGIN, 100, 130, 60), 'Stream')
        self.broadcast_button.on_clicked.connect(self.media_actions)
        self.add_child(self.broadcast_button)
 
        self.webcam_button = ui.Button(ui.Rect(170, 100, 130, 60), 'Webcam')
        self.webcam_button.on_clicked.connect(self.media_actions)
        self.add_child(self.webcam_button)
        
        self.quit_button = ui.Button(ui.Rect(MARGIN, 180, 280, 30), 'Back')
        self.quit_button.on_clicked.connect(self.media_actions)
        self.add_child(self.quit_button)
        
    def media_actions(self, btn, mbtn):
        logger.info(btn.text)
         
        if btn.text == 'Back':
            logger.info('back was clicked!!!')
            ui.scene.push(MenuScreen())
        elif btn.text == 'Radio':
            logger.info('Radio was clicked!!!')
            ui.scene.push(PiRadioScreen())
        elif btn.text == 'Social':
            ui.scene.push(PiSocialScreen())
        elif btn.text == 'Broadcast':
            ui.scene.push(BroadcastScreen())
        elif btn.text == 'Webcam':
            ui.scene.push(WebcamScreen())

    def update(self, dt):
        ui.Scene.update(self, dt)
        
class WebcamScreen(ui.Scene):

    def __init__(self):
        ui.Scene.__init__(self)
        self.capture = cv.CaptureFromCAM(camera_index)
        
        
    def media_actions(self, btn, mbtn):
        logger.info(btn.text)
         
        if btn.text == 'Back':
            logger.info('back was clicked!!!')
            ui.scene.push(MediaScreen())
        elif btn.text == 'Radio':
            logger.info('Radio was clicked!!!')
            ui.scene.push(PiRadioScreen())
        elif btn.text == 'Social':
            ui.scene.push(PiSocialScreen())
        elif btn.text == 'Broadcast':
            ui.scene.push(BroadcastScreen())
        elif btn.text == 'Webcam':
            ui.scene.push(WebcamScreen())

    def update(self, dt):
        ui.Scene.update(self, dt)
        frame = cv.QueryFrame(self.capture)
        if frame is None:
            print "fail with putting in frame"

        else:
            c = cv.WaitKey(100)
            print 'capturing!'
            cv.SaveImage("pictest.png", frame)
            img=ui.pygame.image.load("pictest.png")
            ui.window_surface.blit(img,(0,0))
        
class PiRadioScreen(ui.Scene):

    def __init__(self):
        ui.Scene.__init__(self)
        
        
 
        self.quit_button = ui.Button(ui.Rect(MARGIN, 180, 280, 30), 'Back')
        self.quit_button.on_clicked.connect(self.piradio_actions)
        self.add_child(self.quit_button)
        
    def refresh_menu_screen(self):
        pprint(self)
    #set up the fixed items on the menu
        screen = ui.window_surface
        screen.fill(WHITE) #change the colours if needed
        font=ui.pygame.font.Font(None,24)
        title_font=ui.pygame.font.Font(None,34)
        station_font=ui.pygame.font.Font(None,20)
        label=title_font.render("MPC RADIO", 1, (BLUE))
        label2=font.render("Streaming Internet Radio", 1, (RED))
        screen.blit(label,(105, 15))
        screen.blit(label2,(88, 45))
        play=ui.pygame.image.load("PiRadio/play.tiff")
        pause=ui.pygame.image.load("PiRadio/pause.tiff")
        refresh=ui.pygame.image.load("PiRadio/refresh.tiff")
        previous=ui.pygame.image.load("PiRadio/previous.tiff")
        next=ui.pygame.image.load("PiRadio/next.tiff")
        vol_down=ui.pygame.image.load("PiRadio/volume_down.tiff")
        vol_up=ui.pygame.image.load("PiRadio/volume_up.tiff")
        mute=ui.pygame.image.load("PiRadio/mute.png")
        exit=ui.pygame.image.load("PiRadio/exit.tiff")
        radio=ui.pygame.image.load("PiRadio/radio.tiff")
        # draw the main elements on the screen
        screen.blit(play,(20,80))	
        screen.blit(pause,(80,80))
        ui.pygame.draw.rect(screen, RED, (8, 70, 304, 108),1)
        ui.pygame.draw.line(screen, RED, (8,142),(310,142),1)
        ui.pygame.draw.rect(screen, CREAM, (10, 143, 300, 33),0)
        screen.blit(refresh,(270,70))
        screen.blit(previous,(10,180))
        screen.blit(next,(70,180))
        screen.blit(vol_down,(130,180))
        screen.blit(vol_up,(190,180))
        screen.blit(mute,(250,180))	
        screen.blit(exit,(270,5))
        screen.blit(radio,(2,1))
        ui.pygame.draw.rect(screen, BLUE, (0,0,320,240),3)
        ##### display the station name and split it into 2 parts : 
        station = subprocess.check_output("mpc current", shell=True )
        lines=station.split(":")
        length = len(lines) 
        if length==1:
            line1 = lines[0]
            line1 = line1[:-1]
            line2 = "No additional info: "
        else:
            line1 = lines[0]
            line2 = lines[1]

        line2 = line2[:42]
        line2 = line2[:-1]
        #trap no station data
        if line1 =="":
            line2 = "Press PLAY or REFRESH"
            station_status = "stopped"
            status_font = RED
        else:
            station_status = "playing"
            status_font = GREEN
        station_name=station_font.render(line1, 1, (RED))
        additional_data=station_font.render(line2, 1, (BLUE))
        station_label=title_font.render(station_status, 1, (status_font))
        screen.blit(station_label,(175,100))
        screen.blit(station_name,(13,145))
        screen.blit(additional_data,(12,160))
        ######## add volume number
        volume = subprocess.check_output("mpc volume", shell=True )
        volume = volume[8:]
        volume = volume[:-1]
        volume_tag=font.render(volume, 1, (BLACK))
        screen.blit(volume_tag,(175,75))
        ####### check to see if the Radio is connected to the internet
        IP = subprocess.check_output("hostname -I", shell=True )
        IP=IP[:3]
        if IP =="192":
            network_status = "online"
            status_font = GREEN

        else:
            network_status = "offline"
            status_font = RED

        network_status_label = font.render(network_status, 1, (status_font))
        screen.blit(network_status_label, (215,75))
        ui.pygame.display.flip()
        
    def piradio_actions(self, btn, mbtn):
        logger.info(btn.text)
         
        if btn.text == 'Back':
            logger.info('back was clicked!!!')
            ui.scene.push(MediaScreen())

    def update(self, dt):
        self.refresh_menu_screen()
        ui.Scene.update(self, dt)
         
 
ui.init('BlueArrow UI', (320, 240))
pygame.mouse.set_visible(DEV_MODE)
 
pitft = MainScreen()

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)
         
signal.signal(signal.SIGINT, signal_handler)
 
ui.scene.push(pitft)
ui.run()


