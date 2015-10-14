#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Módulos

# Constantes
import scene


# Clases
# ---------------------------------------------------------------------

class SceneHome(scene.Scene):
    """Escena inicial del juego, esta es la primera que se carga cuando inicia"""
    
    def __init__(self, director):
        scene.Scene.__init__(self, director)
       
    def on_update(self):
        pass

    def on_event(self):
        pass

    def on_draw(self, screen):
        pass

# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------



# ---------------------------------------------------------------------

def main():
	pass

if __name__ == '__main__':
	main()
