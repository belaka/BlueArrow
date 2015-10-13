import sys
 
import pygame
import os
import pygameui as ui
import logging
import signal
import threading
import time

log_format = '%(asctime)-6s: %(name)s - %(levelname)s - %(message)s'
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(log_format))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
 
#os.putenv('SDL_FBDEV', '/dev/fb1')
#os.putenv('SDL_MOUSEDRV', 'TSLIB')
#os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
 
MARGIN = 20

class MainScreen(ui.Scene):
    def __init__(self):
        ui.Scene.__init__(self)
 
        self.system_button = ui.Button(ui.Rect(MARGIN, MARGIN, 130, 60), 'System')
        self.system_button.on_clicked.connect(self.quit_action)
        self.add_child(self.system_button)
        
        self.quit_button = ui.Button(ui.Rect(MARGIN, 180, 280, 30), 'Quit')
        self.quit_button.on_clicked.connect(self.quit_action)
        self.add_child(self.quit_button)
        
    def quit_action(self, btn, mbtn):
        logger.info(btn.text)
        if btn.text == 'System':
            logger.info('system was clicked!!!')
            ui.scene.push(SystemScreen())
        elif btn.text == 'Quit':
            sys.exit()
            
    def update(self, dt):
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
 
        self.connect_button = ui.Button(ui.Rect(170, 100, 130, 60), 'Wifi')
        self.add_child(self.connect_button)
        
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
            ui.scene.push(SystemScreen())
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
        elif btn.text == 'Vehicle':
            ui.scene.push(systemScene)
        elif btn.text == 'Media':
            ui.scene.push(systemScene)
        elif btn.text == 'Wifi':
            ui.scene.push(systemScene)
            
    def update(self, dt):
        ui.Scene.update(self, dt)
 
 
ui.init('BlueArrow UI', (320, 240))
pygame.mouse.set_visible(False)
 
pitft = MainScreen()

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)
         
signal.signal(signal.SIGINT, signal_handler)
 
ui.scene.push(pitft)
ui.run()


