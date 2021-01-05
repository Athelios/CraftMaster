from npc import *
import math
from pyglet import image
from pyglet.graphics import TextureGroup
import os
import json


class Enemy(Npc):
    def __init__(self, world, position, health, dy=0, walkSpeed=5, flying=False, flySpeed=10, height=1, jumpHeight=1.0):
        super(Enemy, self).__init__(world, position, health, dy, walkSpeed, flying, flySpeed, height, jumpHeight)
        self.model = self.createModel(world)
        self.rotateSelfY(-math.pi/2)
        with open(os.path.join('animation', 'enemy.anim'), 'r') as file:
            self.animation = json.load(file)
        self.frames = [0, 0, 0]
        self.attacking = False

    def createModel(self, world):
        texture0 = TextureGroup(image.load(os.path.join("texture", "zombie0.png")).get_texture())
        texture1 = TextureGroup(image.load(os.path.join("texture", "zombie1.png")).get_texture())

        x, y, z = self.position

        cube1 = createCube(world, texture0, x + 0.15, y + 0.15, z, 0.29, 0.7, 0.25)
        cube2 = createCube(world, texture0, x - 0.15, y + 0.15, z, 0.29, 0.7, 0.25)
        cube3 = createCube(world, texture0, x, y + 0.8, z, 0.6, 0.7, 0.3)
        cube4 = createCube(world, texture0, x + 0.4, y + 0.8, z, 0.2, 0.7, 0.2)
        cube5 = createCube(world, texture0, x - 0.4, y + 0.8, z, 0.2, 0.7, 0.2)
        cube6 = createCube(world, texture1, x, y + 1.3, z, 0.5, 0.5, 0.5)

        model = [cube1, cube2, cube3, cube4, cube5, cube6]

        return model

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
        player.hit(vector)
        self.attacking = True
        self.energy = 0

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
        if self.distanceTo(world.player) <= 3:
            delta = [world.player.position[0] - self.position[0], world.player.position[1] - self.position[1], world.player.position[2] - self.position[2]]
        theta = self.angle(self.sight, [delta[0], delta[2]])
        if delta[0] != 0 or delta[2] != 0:
            self.rotateSelfY(theta)
            self.sight = [delta[0], delta[2]]
        self.lastPosition = list(self.position)
        self.counter += 1
        self.energy = min(self.energy + 2, 100)
        self.animate()
        super(Enemy, self).update(dt, world)
