from pyglet.gl import *

# Direct OpenGL commands to this window.
window = pyglet.window.Window(1200,700)


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_TRIANGLES)
    glVertex2f(0, 0,1)
    glVertex2f(0, window.height/2,3)
    glVertex2f(window.width, window.height,5)
    glEnd()
    pyglet.graphics.draw(2, pyglet.gl.GL_POINTS,('v3f', (10.0, 15.0, 0.0, 30.0, 35.0, 0.0)))
pyglet.app.run()
