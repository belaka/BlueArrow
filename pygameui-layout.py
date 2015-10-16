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
import datetime
from wifi import *
from pprint import pprint

log_format = '%(asctime)-6s: %(name)s - %(levelname)s - %(message)s'
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(log_format))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

DEV_MODE = True

if DEV_MODE ==  False:
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')


 
LIST_WIDTH = 280
MARGIN = 20
SMALL_MARGIN = 10

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
        self.clock.tick(0)
        self.clock_button = ui.Button(ui.Rect(MARGIN, MARGIN, 280, 60), str(time.strftime("%Y-%m-%d %H:%M:%S")))
        self.clock_button.on_clicked.connect(self.main_action)
        self.add_child(self.clock_button)
        ui.Scene.update(self, dt)


class MenuScreen(ui.Scene):

    def __init__(self):
        ui.Scene.__init__(self)
 
        self.system_button = ui.Button(ui.Rect(MARGIN, MARGIN, 130, 60), 'System')
        self.system_button.on_clicked.connect(self.home_button)
        self.add_child(self.system_button)
 
        self.vehicle_button = ui.Button(ui.Rect(170, MARGIN, 130, 60), 'Vehicle')
        self.add_child(self.vehicle_button)
 
        self.media_button = ui.Button(ui.Rect(MARGIN, 100, 130, 60), 'Media')
        self.add_child(self.media_button)
 
        self.wifi_button = ui.Button(ui.Rect(170, 100, 130, 60), 'Wifi')
        self.wifi_button.on_clicked.connect(self.home_button)
        self.add_child(self.wifi_button)
        
        self.quit_button = ui.Button(ui.Rect(MARGIN, 180, 280, 30), 'Quit')
        self.quit_button.on_clicked.connect(self.home_button)
        self.add_child(self.quit_button)
        
    def home_button(self, btn, mbtn):
        logger.info(btn.text)
         
        if btn.text == 'System':
            logger.info('system was clicked!!!')
            ui.scene.push(SystemScreen())
        elif btn.text == 'Vehicle':
            ui.scene.push(SystemScreen())
        elif btn.text == 'Media':
            ui.scene.push(SystemScreen())
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
            ui.scene.push(MainScreen())
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
 
 
ui.init('BlueArrow UI', (320, 240))
pygame.mouse.set_visible(DEV_MODE)
 
pitft = MainScreen()

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)
         
signal.signal(signal.SIGINT, signal_handler)
 
ui.scene.push(pitft)
ui.run()


