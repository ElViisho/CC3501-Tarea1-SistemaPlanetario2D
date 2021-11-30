"""

"""

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es
import numpy as np

from OpenGL.GL import glClearColor
from typing import List

import json


class Body(object):
    listaSat: List['Body']
    
    def __init__(self, data, parent):
        # Figuras básicas
        self.color = data[" Color"]
        self.radio = data[" Radius"]
        self.dist = data[" Distance"]
        self.velocity = data[" Velocity"]
        if data[" Satellites"] != " Null":
            self.sateliteData = []
            for i in data[" Satellites"]:
                self.sateliteData.append(i)
        else:
            self.sateliteData = " Null"

        self.parent = parent
        
        gpu_body = es.toGPUShape(bs.createColorCircle(self.radio, self.color[0], self.color[1], self.color[2]))
        
        cuerpo = sg.SceneGraphNode('cuerpo')
        cuerpo.transform = tr.translate(self.dist, 0 ,0)
        cuerpo.childs += [gpu_body]

        local = sg.SceneGraphNode('local')
        local.childs += [cuerpo]
        
        self.model = local

        gpu_sel = es.toGPUShape(bs.createColorCircle(self.radio*1.1+.005, 1.0, 1.0, 1.0))

        selCircle = sg.SceneGraphNode('selCircle')
        selCircle.transform = tr.translate(self.dist, 0 ,0)
        selCircle.childs += [gpu_sel]

        selCircleTR = sg.SceneGraphNode('selCircleTR')
        selCircleTR.childs += [selCircle]
        
        self.circle = selCircleTR

        self.select = 0

    def draw(self, pipeline):
        if self.select == 1:
            sg.drawSceneGraphNode(self.circle, pipeline, 'transform')
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

    def update(self, theta, zoom, posX, posY):
        self.circle.transform = tr.matmul([tr.translate(posX, posY, 0),
                    tr.rotationZ(self.velocity*theta), 
                    tr.uniformScale(zoom)])
        self.model.transform = tr.matmul([tr.translate(posX, posY, 0),
                    tr.rotationZ(self.velocity*theta), 
                    tr.uniformScale(zoom)])
        if self.parent!=None:
            self.model.transform = tr.matmul([
                tr.translate(self.parent.dist*np.cos(self.parent.velocity*theta)*zoom + posX, 
                            self.parent.dist*np.sin(self.parent.velocity*theta)*zoom + posY, 0),
                tr.rotationZ((self.velocity-self.parent.velocity)*theta),
                tr.uniformScale(zoom)])
            self.circle.transform = tr.matmul([
                tr.translate(self.parent.dist*np.cos(self.parent.velocity*theta)*zoom + posX, 
                            self.parent.dist*np.sin(self.parent.velocity*theta)*zoom + posY, 0),
                tr.rotationZ((self.velocity-self.parent.velocity)*theta),
                tr.uniformScale(zoom)])


class Orbita(object):

    def __init__(self, radio, x0, y0, vel):

        self.radio = radio
        self.velocity = vel

        gpu_orbit = es.toGPUShape(bs.createOrbit(self.radio, x0, y0))
        
        orbita = sg.SceneGraphNode('orbita')
        orbita.childs += [gpu_orbit]

        orbitaTR = sg.SceneGraphNode('orbitaTR')
        orbitaTR.childs += [orbita]

        self.model = orbitaTR

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

    def update(self, theta, zoom, posX, posY):
        self.model.transform = tr.matmul([tr.translate(posX, posY, 0), tr.rotationZ(self.velocity*theta), tr.uniformScale(zoom)])



class Bodies(object):
    bodies: List['Body']

    def __init__(self):
        self.bodies = []
        self.orbits = []
        self.bodyCount = 0

    def createBodies(self, data, parent):
        self.bodies.append(Body(data, parent))
        self.bodyCount += 1
        ThisBody = Body(data, parent)
        n = len(ThisBody.sateliteData)
        i = 0
        while i<n:
            if ThisBody.sateliteData[i] != " Null":
                if isinstance(ThisBody.sateliteData[i], str):
                    return
                NewBody = ThisBody.sateliteData[i]
                self.orbits.append(Orbita(NewBody[" Distance"], ThisBody.dist, 0, ThisBody.velocity))
                NewBody[" Velocity"] += ThisBody.velocity
                Bodies.createBodies(self, NewBody, ThisBody)
            i += 1

        todo = sg.SceneGraphNode('todo')
        for i in self.bodies:
            todo.childs += [i]
        for j in self.orbits:
            todo.childs += [j]

        

    def draw(self, pipeline):
        for l in self.orbits:
            l.draw(pipeline)
        for k in self.bodies:
            k.draw(pipeline)
        
    def update(self, theta, zoom, posX, posY, currentSel):
        for j in self.orbits:
            j.update(theta, zoom, posX, posY)
        k = 0
        while k < len(self.bodies):
            self.bodies[k].update(theta, zoom, posX, posY)
            if k == currentSel:
                self.bodies[k].select = 1
            else:
                self.bodies[k].select = 0 
            k += 1