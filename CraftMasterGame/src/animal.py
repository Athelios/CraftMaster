from npc import *
import math
from pyglet import image
from pyglet.graphics import TextureGroup
import os
import json
import random


class Animal(Npc):
    def __init__(self, world, position, health, dy=0, walkSpeed=5, flying=False, flySpeed=10, height=1, jumpHeight=1.0):
        super(Animal, self).__init__(world, position, health, dy, walkSpeed, flying, flySpeed, height, jumpHeight)
        self.model = self.createModel(world)
        self.rotateSelfY(-math.pi/2)
        with open(os.path.join('animation', 'animal.anim'), 'r') as file:
            self.animation = json.load(file)
        self.frames = [0, 0, 0, 0]
        self.running = False

    def createModel(self, world):
        texture0 = TextureGroup(image.load(os.path.join("texture", "sheep0.png")).get_texture())
        texture1 = TextureGroup(image.load(os.path.join("texture", "sheep1.png")).get_texture())

        x, y, z = self.position

        cube1 = createCube(world, texture0, x + 0.15, y, z + 0.3, 0.24, 0.5, 0.2)
        cube2 = createCube(world, texture0, x - 0.15, y, z + 0.3, 0.24, 0.5, 0.2)
        cube3 = createCube(world, texture0, x + 0.15, y, z - 0.3, 0.24, 0.5, 0.2)
        cube4 = createCube(world, texture0, x - 0.15, y, z - 0.3, 0.24, 0.5, 0.2)
        cube5 = createCube(world, texture0, x, y + 0.5, z, 0.55, 0.5, 0.85)
        cube6 = createCube(world, texture1, x, y + 0.9, z + 0.4, 0.4, 0.4, 0.4)

        model = [cube1, cube2, cube3, cube4, cube5, cube6]

        return model

    def hit(self, direction):
        self.running = True
        self.hitdir = direction
        self.stunned = 30
        x = self.position[0] + random.randint(-10, 10)
        z = self.position[2] + random.randint(-10, 10)
        y = self.world.getZ(x, z)
        self.goal = [x, y, z]
        self.navigation.navigate()

    def ai(self, world):
        if self.running:
            if self.counter % 120 == 0:
                x = self.position[0] + random.randint(-10, 10)
                z = self.position[2] + random.randint(-10, 10)
                y = self.world.getZ(x, z)
                self.goal = [x, y, z]
                self.navigation.navigate()
        else:
            if self.counter % 120 == 0:
                x = self.position[0] + random.randint(-1, 1)
                z = self.position[2] + random.randint(-1, 1)
                y = self.world.getZ(x, z)
                self.goal = [x, y, z]
                self.navigation.navigate()

    def update(self, dt, world):
        if not self.stunned:
            self.ai(world)
            if self.goal:
                self.navigate()
        else:
            if self.stunned == 1:
                self.goal = list(self.world.player.position)
                self.navigation.navigate()
        delta = [self.position[0] - self.lastPosition[0], self.position[1] - self.lastPosition[1], self.position[2] - self.lastPosition[2]]
        for shape in self.model:
            for part in shape:
                for i in range(0, len(part.vertices), 3):
                    part.vertices[i] += delta[0]
                    part.vertices[i + 1] += delta[1]
                    part.vertices[i + 2] += delta[2]
        walk = delta[0] != 0 or delta[2] != 0
        self.walking = self.walking or walk
        theta = self.angle(self.sight, [delta[0], delta[2]])
        if delta[0] != 0 or delta[2] != 0:
            self.rotateSelfY(theta)
            self.sight = [delta[0], delta[2]]
        self.lastPosition = list(self.position)
        self.counter += 1
        self.energy = min(self.energy + 2, 100)
        self.animate()
        super(Animal, self).update(dt, world)
