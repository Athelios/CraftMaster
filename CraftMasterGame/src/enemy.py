from npc import Npc
import math
from pyglet.gl import *
from navigation import *
from pyglet import image
from pyglet.graphics import TextureGroup
import os


def createCube(world, texture, x, y, z, sx=1.0, sy=1.0, sz=1.0):
    x, y, z = x - sx*0.5, y - sy*0.5, z - sz*0.5
    X, Y, Z = x + sx*1, y + sy*1, z + sz*1
    #tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1,))
    tex_coords1 = ('t2f', (0.0/8, 0, 1.0/8, 0, 1.0/8, 1, 0.0/8, 1,))
    tex_coords2 = ('t2f', (1.0/8, 0, 2.0/8, 0, 2.0/8, 1, 1.0/8, 1,))
    tex_coords3 = ('t2f', (2.0/8, 0, 3.0/8, 0, 3.0/8, 1, 2.0/8, 1,))
    tex_coords4 = ('t2f', (3.0/8, 0, 4.0/8, 0, 4.0/8, 1, 3.0/8, 1,))
    tex_coords5 = ('t2f', (4.0/8, 0, 5.0/8, 0, 5.0/8, 1, 4.0/8, 1,))
    tex_coords6 = ('t2f', (5.0/8, 0, 6.0/8, 0, 6.0/8, 1, 5.0/8, 1,))
    cube = [world.batch.add(4, GL_QUADS, texture, ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z,)), tex_coords5),
            world.batch.add(4, GL_QUADS, texture, ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z,)), tex_coords3),
            world.batch.add(4, GL_QUADS, texture, ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z,)), tex_coords6),
            world.batch.add(4, GL_QUADS, texture, ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z,)), tex_coords1),
            world.batch.add(4, GL_QUADS, texture, ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z,)), tex_coords4),
            world.batch.add(4, GL_QUADS, texture, ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z,)), tex_coords2)]

    return cube


class Enemy(Npc):
    def __init__(self, world, position, health, dy=0, walkSpeed=5, flying=False, flySpeed=10, height=1, jumpHeight=1.0):
        super(Enemy, self).__init__(world, position, health, dy, walkSpeed, flying, flySpeed, height, jumpHeight)
        self.lastPosition = list(position)
        self.model = self.createModel(world)
        #self.rotate(3.14/4, 0, 0)
        self.navigation = Navigation(self)

        self.SEEK_MAX = 100

    def createModel(self, world):
        texture0 = TextureGroup(image.load(os.path.join("texture", "zombie0.png")).get_texture())
        texture1 = TextureGroup(image.load(os.path.join("texture", "zombie1.png")).get_texture())

        x, y, z = self.position
        cube1 = createCube(world, texture0, x + 0.15, y - 0.15, z, 0.29, 0.7, 0.25)
        cube2 = createCube(world, texture0, x - 0.15, y - 0.15, z, 0.29, 0.7, 0.25)
        cube3 = createCube(world, texture0, x, y + 0.5, z, 0.6, 0.7, 0.3)
        cube4 = createCube(world, texture0, x + 0.4, y + 0.5, z, 0.2, 0.7, 0.2)
        cube5 = createCube(world, texture0, x - 0.4, y + 0.5, z, 0.2, 0.7, 0.2)
        cube6 = createCube(world, texture1, x, y + 1, z, 0.5, 0.5, 0.5)

        model = cube1 + cube2 + cube3 + cube4 + cube5 + cube6

        return model

    def moveTo(self, position):
        self.goal = position
        self.navigation.navigate()
        # self.graph = Graph(self.position, position, self.SEEK_DIST)

    def navigate(self):
        self.position = self.navigation.move()

    def update(self, dt, world):
        if self.goal:
            self.navigate()
        for part in self.model:
            for i in range(0, len(part.vertices), 3):
                part.vertices[i] += self.position[0] - self.lastPosition[0]
            for i in range(1, len(part.vertices), 3):
                part.vertices[i] += self.position[1] - self.lastPosition[1]
            for i in range(2, len(part.vertices), 3):
                part.vertices[i] += self.position[2] - self.lastPosition[2]
        self.lastPosition = list(self.position)

    
