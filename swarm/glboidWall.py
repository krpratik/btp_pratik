
from __future__ import division, print_function, absolute_import, unicode_literals

from pyglet import *
from pyglet.gl import *
from math import *
import boidsWall 

class World(object):
    verts = [0.5, 0.0, -0.5, -0.2, -0.5, 0.2]
    vertsGl = (GLfloat * len(verts))(*verts)

    def __init__(self, swarm, offx, offy):
        self.swarm = swarm
        self.ents = swarm.boids  # this will point to a list of boids
        self.ent_size = 15.0
        self.num_ents = len(swarm.boids)
        self.fps = clock.ClockDisplay()
        self.o_x = offx
        self.o_y = offy

    def draw_entity(self, e):
        """ Draws a boid """
        glLoadIdentity()
        glTranslatef(e.position.x + self.o_x, e.position.y + self.o_y, 0.0)
        glRotatef(e.rotation*180 / pi, 0, 0, 1)
        glScalef(self.ent_size, self.ent_size, 1.0)
        glColor4f(0, 0, 0, 0)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, self.vertsGl)
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertsGl) // 2)

    def draw_grid(self):
        cw = self.swarm.cell_width
        w = cw * self.swarm.divisions_width
        w2 = cw * self.swarm.divisions_height
        for i in range(self.swarm.divisions_height):
            xy = i*cw
            glLoadIdentity()
            glBegin(GL_LINES)
            glColor4f(0.5, 0.5, 0.5, 0)
            glVertex2f(0, xy)
            glVertex2f(w, xy)
            glEnd()
        for i in range(self.swarm.divisions_width):
            xy = i*cw
            glBegin(GL_LINES)
            glColor4f(0.5, 0.5, 0.5, 0)
            glVertex2f(xy, 0)
            glVertex2f(xy, w2)
            glEnd()

    def draw(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.fps.draw()

        #self.draw_grid()
        for ent in self.ents:
            self.draw_entity(ent)

sim = boidsWall.FlockSimulation(80,1300,700)
world = World(sim.swarm, -25, -25)

window = pyglet.window.Window(1300,700, vsync=False)


@window.event
def on_draw():
    window.clear()
    world.draw()


def update(dt):
    sim.update(dt)


def idle(dt):
    pass

clock.schedule(update)
clock.schedule(idle)

if __name__ == '__main__':
    pyglet.app.run()
