from npc import Npc
import math
from pyglet.gl import *
from navigation import *
from pyglet import image
from pyglet.graphics import TextureGroup
import os
import json


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
        self.rotateY(-math.pi/2)
        #self.rotateZ(self.model[0], [0, 0.5, 0], -math.pi/4)
        self.navigation = Navigation(self)
        self.counter = 0
        self.energy = 100
        with open(os.path.join('animation', 'enemy.anim'), 'r') as file:
            self.animation = json.load(file)
        self.frame = 0

        self.SEEK_MAX = 100

    def createModel(self, world):
        texture0 = TextureGroup(image.load(os.path.join("texture", "zombie0.png")).get_texture())
        texture1 = TextureGroup(image.load(os.path.join("texture", "zombie1.png")).get_texture())

        x, y, z = self.position
        """
        cube1 = createCube(world, texture0, x + 0.15, y - 0.15, z, 0.29, 0.7, 0.25)
        cube2 = createCube(world, texture0, x - 0.15, y - 0.15, z, 0.29, 0.7, 0.25)
        cube3 = createCube(world, texture0, x, y + 0.5, z, 0.6, 0.7, 0.3)
        cube4 = createCube(world, texture0, x + 0.4, y + 0.5, z, 0.2, 0.7, 0.2)
        cube5 = createCube(world, texture0, x - 0.4, y + 0.5, z, 0.2, 0.7, 0.2)
        cube6 = createCube(world, texture1, x, y + 1, z, 0.5, 0.5, 0.5)
        """

        """
        cube1 = createCube(world, texture0, x + 0.15, y - 0.15, z, 0.29, 0.7, 0.25)
        cube2 = createCube(world, texture0, x - 0.15, y - 0.15, z, 0.29, 0.7, 0.25)
        cube3 = createCube(world, texture0, x, y + 0.5, z, 0.6, 0.7, 0.3)
        cube4 = createCube(world, texture0, x + 0.4, y + 0.5, z, 0.2, 0.7, 0.2)
        cube5 = createCube(world, texture0, x - 0.4, y + 0.5, z, 0.2, 0.7, 0.2)
        cube6 = createCube(world, texture1, x, y + 1, z, 0.5, 0.5, 0.5)
        """

        cube1 = createCube(world, texture0, x + 0.15, y + 0.15, z, 0.29, 0.7, 0.25)
        cube2 = createCube(world, texture0, x - 0.15, y + 0.15, z, 0.29, 0.7, 0.25)
        cube3 = createCube(world, texture0, x, y + 0.8, z, 0.6, 0.7, 0.3)
        cube4 = createCube(world, texture0, x + 0.4, y + 0.8, z, 0.2, 0.7, 0.2)
        cube5 = createCube(world, texture0, x - 0.4, y + 0.8, z, 0.2, 0.7, 0.2)
        cube6 = createCube(world, texture1, x, y + 1.3, z, 0.5, 0.5, 0.5)

        model = [cube1, cube2, cube3, cube4, cube5, cube6]

        return model

    def moveTo(self, position):
        self.goal = position
        self.navigation.navigate()
        # self.graph = Graph(self.position, position, self.SEEK_DIST)

    def navigate(self):
        self.position = self.navigation.move()

    def distanceTo(self, object):
        x1, y1, z1 = self.position
        x2, y2, z2 = object.position
        return (((x2 - x1) ** 2) + ((y2 - y1) ** 2) + ((z2 - z1) ** 2)) ** (1 / 2)

    def ai(self, world):
        if 2 < self.distanceTo(world.player) < 20:
            self.goal = list(world.player.position)
            self.goal = (int(round(self.goal[0])), int(round(self.goal[1])) - 1, int(round(self.goal[2])))
            if self.counter % 20 == 0:
                self.navigation.navigate()
        elif self.distanceTo(world.player) <= 2:
            self.goal = None
            if self.energy == 100:
                self.attack(world.player)
        else:
            self.goal = None

    def attack(self, player):
        vector = [10*(player.position[0] - self.position[0]), 10*(player.position[2] - self.position[2]), 10]
        #player.hit(vector)
        self.energy = 0

    def lerp(self, frame1, frame2, alpha):
        x1, y1, z1 = frame1
        x2, y2, z2 = frame2
        x = x1 + (x2 - x1) * alpha
        y = y1 + (y2 - y1) * alpha
        z = z1 + (z2 - z1) * alpha
        return x, y, z

    def animate(self):
        index = self.animation['index']
        origin = self.animation['origin']
        keyframes = self.animation['keyframes']
        #last = keyframes[len(keyframes) - 1][0]
        rot = self.lerp(keyframes[math.floor(self.frame / 30)], keyframes[math.ceil(self.frame / 30)], (self.frame / 30) % 1)
        self.rotateZ(self.model[index], origin, math.sin(self.rotation[0])*rot[2])
        self.rotateX(self.model[index], origin, math.cos(self.rotation[0])*rot[2])
        self.frame += 1
        if self.frame == 120:
            self.frame = 0

    def update(self, dt, world):
        self.ai(world)
        if self.goal:
            self.navigate()
        delta = [self.position[0] - self.lastPosition[0], self.position[1] - self.lastPosition[1], self.position[2] - self.lastPosition[2]]
        for shape in self.model:
            for part in shape:
                for i in range(0, len(part.vertices), 3):
                    part.vertices[i] += delta[0]
                    part.vertices[i + 1] += delta[1]
                    part.vertices[i + 2] += delta[2]
        if self.distanceTo(world.player) <= 3:
            delta = [world.player.position[0] - self.position[0], world.player.position[1] - self.position[1], world.player.position[2] - self.position[2]]
        theta = self.angle(self.sight, [delta[0], delta[2]])
        if delta[0] != 0 or delta[2] != 0:
            self.rotateY(theta)
            self.sight = [delta[0], delta[2]]
        self.lastPosition = list(self.position)
        self.counter += 1
        self.energy = min(self.energy + 2, 100)
        self.animate()
        super(Enemy, self).update(dt, world)

    def angle(self, v1, v2):
        angle = math.atan2(v2[1], v2[0]) - math.atan2(v1[1], v1[0])
        return angle

    def rotateX(self, model, origin, theta):
        for part in model:
            for i in range(0, len(part.vertices), 3):
                oy = origin[1] + self.position[1]
                oz = origin[2] + self.position[2]
                y = oy + math.cos(theta) * (part.vertices[i + 1] - oy) - math.sin(theta) * (part.vertices[i + 2] - oz)
                z = oz + math.sin(theta) * (part.vertices[i + 1] - oy) + math.cos(theta) * (part.vertices[i + 2] - oz)
                part.vertices[i + 1] = y
                part.vertices[i + 2] = z

    def rotateZ(self, model, origin, theta):
        for part in model:
            for i in range(0, len(part.vertices), 3):
                ox = origin[0] + self.position[0]
                oy = origin[1] + self.position[1]
                x = ox + math.cos(theta) * (part.vertices[i] - ox) - math.sin(theta) * (part.vertices[i + 1] - oy)
                y = oy + math.sin(theta) * (part.vertices[i] - ox) + math.cos(theta) * (part.vertices[i + 1] - oy)
                part.vertices[i + 0] = x
                part.vertices[i + 1] = y

    def rotateY(self, theta):
        for shape in self.model:
            for part in shape:
                for i in range(0, len(part.vertices), 3):
                    #position = [self.position[0], self.position[1], self.position[2]]
                    #part.vertices[i] = position[0] + math.cos(x) * (part.vertices[i] - position[0]) - math.sin(x) * (part.vertices[i+2] - position[2])
                    x = self.position[0] + math.cos(theta) * (part.vertices[i] - self.position[0]) - math.sin(theta) * (part.vertices[i + 2] - self.position[2])
                    # position = [self.position[0], self.position[1], self.position[2]]
                    # part.vertices[i] = position[2] + math.sin(x) * (part.vertices[i-2] - position[0]) + math.cos(x) * (part.vertices[i] - position[2])
                    z = self.position[2] + math.sin(theta) * (part.vertices[i] - self.position[0]) + math.cos(theta) * (part.vertices[i + 2] - self.position[2])
                    part.vertices[i] = x
                    part.vertices[i + 2] = z

                    """
                    d = math.hypot(part.vertices[i + 2], part.vertices[i])
                    dd = d**0.5
                    theta = dd*x
                    part.vertices[i] = math.cos(theta) * part.vertices[i] - math.sin(theta) * part.vertices[i + 2]
                    part.vertices[i + 2] = math.sin(theta) * part.vertices[i] + math.cos(theta) * part.vertices[i + 2]
                    """

                    """
                    cx = 0
                    cz = 0
                    x = part.vertices[i] - cx
                    z = part.vertices[i + 2] - cz
                    d = math.hypot(z, x)
                    theta = math.atan2(z, x) + x
                    part.vertices[i] = cx + d * math.cos(theta)
                    part.vertices[i + 2] = cz + d * math.sin(theta)
                    """
        self.rotation = (self.rotation[0] + theta, self.rotation[1])
