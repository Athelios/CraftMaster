from npc import Npc
import math
from pyglet.gl import *
from navigation import *

class Enemy(Npc):
    def __init__(self, world, position, health, dy=0, walkSpeed=5, flying=False, flySpeed=10, height=1, jumpHeight=1.0):
        super(Enemy, self).__init__(world, position, health, dy, walkSpeed, flying, flySpeed, height, jumpHeight)
        self.lastPosition = list(position)
        self.model = self.createModel(world)
        self.counter = 0
        self.navigation = Navigation(self)

        self.SEEK_MAX = 100

    def createModel(self, world):
        x, y, z = self.position
        x, y, z = x - 0.5, y - 0.5, z - 0.5
        X, Y, Z = x + 1, y + 1, z + 1
        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1,))

        color = glColor3ub(255, 0, 0)

        model = [world.batch.add(4, GL_QUADS, color, ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z,)), tex_coords),
                 world.batch.add(4, GL_QUADS, color, ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z,)), tex_coords),
                 world.batch.add(4, GL_QUADS, color, ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z,)), tex_coords),
                 world.batch.add(4, GL_QUADS, color, ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z,)), tex_coords),
                 world.batch.add(4, GL_QUADS, color, ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z,)), tex_coords),
                 world.batch.add(4, GL_QUADS, color, ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z,)), tex_coords)]

        return model

    def moveTo(self, position):
        self.goal = position
        self.navigation.navigate()
        #self.graph = Graph(self.position, position, self.SEEK_DIST)

    def navigate(self):
        self.position = self.navigation.move()

    def update(self, dt, world):
        if self.goal and self.counter % 10 == 0:
            self.navigate()
        for part in self.model:
            for i in range(0, len(part.vertices), 3):
                part.vertices[i] += self.position[0] - self.lastPosition[0]
            for i in range(1, len(part.vertices), 3):
                part.vertices[i] += self.position[1] - self.lastPosition[1]
            for i in range(2, len(part.vertices), 3):
                part.vertices[i] += self.position[2] - self.lastPosition[2]
        self.lastPosition = list(self.position)
        self.counter += 1
