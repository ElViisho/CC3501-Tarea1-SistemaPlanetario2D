"""
Clase controlador, obtiene el input, lo procesa, y manda los mensajes
a los modelos.
"""

import glfw
import sys
from modelos import Body, Bodies

class Controller(object):

    def __init__(self):
        self.zoom = 1
        self.minZoom = 1
        self.maxZoom = 3
        self.zoomSpeed = 0.1

        self.posX = 0
        self.posY = 0
        self.maxPos = 1
        self.moveSpeed = 0.1

        self.sel = 0
        self.selMax = 0
        self.selected = False
        

    def on_key(self, window, key, scancode, action, mods):

        if key == glfw.KEY_ESCAPE:
            sys.exit()

        # Zoom acercar
        elif key == glfw.KEY_Z:
            self.zoom += self.zoomSpeed
            if (self.zoom > self.maxZoom): self.zoom = self.maxZoom
        # Zoom alejar
        elif key == glfw.KEY_X:
            self.zoom -= self.zoomSpeed
            if (self.zoom < self.minZoom): self.zoom = self.minZoom

        # Moverse a la derecha
        elif key == glfw.KEY_A and action == glfw.PRESS:
            self.posX += self.moveSpeed
            if (self.posX > self.maxPos): self.posX = self.maxPos
        # Moverse a la izquierda
        elif key == glfw.KEY_D and action == glfw.PRESS:
            self.posX -= self.moveSpeed
            if (self.posX < -self.maxPos): self.posX = -self.maxPos
        # Moverse hacia arriba
        elif key == glfw.KEY_S and action == glfw.PRESS:
            self.posY += self.moveSpeed
            if (self.posY > self.maxPos): self.posY = self.maxPos
        # Moverse hacia abajo
        elif key == glfw.KEY_W and action == glfw.PRESS:
            self.posY -= self.moveSpeed
            if (self.posY < -self.maxPos): self.posY = -self.maxPos
            
        # Cambiar selección
        elif key == glfw.KEY_RIGHT and action == glfw.PRESS:
            self.sel += 1
            if self.sel >= self.selMax:
                self.sel = 0
        # Cambiar selección
        elif key == glfw.KEY_LEFT and action == glfw.PRESS:
            self.sel -= 1
            if self.sel < 0:
                self.sel = self.selMax - 1
        
        # Elegir un cuerpo
        elif key == glfw.KEY_ENTER and action == glfw.PRESS:
            self.selected = not self.selected

    def update(self):
        self.maxPos = self.zoom-1
        if (self.posX > self.maxPos): self.posX = self.maxPos
        if (self.posX < -self.maxPos): self.posX = -self.maxPos
        if (self.posY > self.maxPos): self.posY = self.maxPos
        if (self.posY < -self.maxPos): self.posY = -self.maxPos
