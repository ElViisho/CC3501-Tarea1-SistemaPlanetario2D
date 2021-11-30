"""
Esta es la clase vista. Contiene el ciclo de la aplicación y ensambla
las llamadas para obtener el dibujo de la escena.
"""

import glfw
from OpenGL.GL import *
import sys
import easy_shaders as es
import basic_shapes as bs
import transformations as tr
import numpy as np

from modelos import *
from controller import Controller

archivo = sys.argv[1]

if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 600
    height = 600

    window = glfw.create_window(width, height, 'Sistema Planetario', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    controlador = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controlador.on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipelineFiguras = es.SimpleTransformShaderProgram()
    pipelineTexturas = es.SimpleTextureTransformShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.05, 0.05, 0.08, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    bodies = Bodies()

    with open(archivo) as bodyData:
        bData = json.load(bodyData)

    bodies.createBodies(bData, None)
    gpuFondo = es.toGPUShape(bs.createTextureQuad("fondoEstrellado.png"), GL_REPEAT, GL_NEAREST)
    gpuInfo = es.toGPUShape(bs.createTextureQuad("InfoPlanetas.jpg"), GL_REPEAT, GL_NEAREST)
    gpuCuadInfo = es.toGPUShape(bs.createTextureQuad("CuadradoInfo.jpg"), GL_REPEAT, GL_NEAREST)

    
    barritasFrames = []
    for i in range(8):
        barritasFrames.append("animacionBarritas\\frame" + str(i+1) + ".jpg")

    controlador.selMax = bodies.bodyCount

    while not glfw.window_should_close(window):  # Dibujando --> 1. obtener el input

        # Using GLFW to check for input events
        glfw.poll_events()  # OBTIENE EL INPUT --> CONTROLADOR --> MODELOS

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Telling OpenGL to use our shader program
        glUseProgram(pipelineTexturas.shaderProgram)

        # Drawing the shapes
        glUniformMatrix4fv(glGetUniformLocation(pipelineTexturas.shaderProgram, "transform"), 1, GL_TRUE, tr.uniformScale(2))
        pipelineTexturas.drawShape(gpuFondo)

        # Telling OpenGL to use our shader program
        glUseProgram(pipelineFiguras.shaderProgram)

        # Theta para la rotacion
        theta = -10 * glfw.get_time()

        # Zoom de las figuras
        zoom = controlador.zoom
        
        # Posicion x de las figuras
        posX = controlador.posX
        # Posicion y de las figuras
        posY = controlador.posY

        controlador.update()
        currentSel = controlador.sel

        # Dibujar los modelos
        bodies.update(theta, zoom, posX, posY, currentSel)
        bodies.draw(pipelineFiguras)

        if controlador.selected == True:
            glUseProgram(pipelineTexturas.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(pipelineTexturas.shaderProgram, "transform"), 
                    1, GL_TRUE, tr.matmul([tr.translate(.35,-0.3, 0), tr.scale(1, .75, 0)]))
            pipelineTexturas.drawShape(gpuInfo)
            glUniformMatrix4fv(glGetUniformLocation(pipelineTexturas.shaderProgram, "transform"), 
                    1, GL_TRUE, tr.matmul([tr.translate(.35, .5, 0), tr.scale(1, .5, 0)]))
            pipelineTexturas.drawShape(gpuCuadInfo)

            color = bodies.bodies[controlador.sel].color
            radio = bodies.bodies[controlador.sel].radio

            gpuBody = es.toGPUShape(bs.createColorCircle(radio, color[0], color[1], color[2]))
            bodyInfo = sg.SceneGraphNode('bodyInfo')
            bodyInfo.transform = tr.translate(.1, .5, 0)
            bodyInfo.childs += [gpuBody]

            i = round(theta)%8

            gpuBarras = es.toGPUShape(bs.createTextureQuad(barritasFrames[i]), GL_REPEAT, GL_NEAREST)
            glUniformMatrix4fv(glGetUniformLocation(pipelineTexturas.shaderProgram, "transform"), 
                    1, GL_TRUE, tr.matmul([tr.translate(.55, .5, 0), tr.scale(.4, .4, 0)]))
            pipelineTexturas.drawShape(gpuBarras)

            glUseProgram(pipelineFiguras.shaderProgram)
            sg.drawSceneGraphNode(bodyInfo, pipelineFiguras, 'transform')

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()
