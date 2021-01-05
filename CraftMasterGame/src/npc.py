from creature import Creature
import math

from pyglet.gl import *

from navigation import *

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


class Npc(Creature):
    def __init__(self, world, position, health, dy=0, walkSpeed=5, flying=False, flySpeed=10, height=1, jumpHeight=1.0):
        self.world = world
        self.lastPosition = list(position)
        self.goal = None
        self.walking = False
        self.navigation = Navigation(self)
        self.counter = 0
        self.energy = 100
        self.SEEK_MAX = 100
        super(Npc, self).__init__(position, health, dy, walkSpeed, flying, flySpeed, height, jumpHeight)

    def navigate(self):
        self.position = self.navigation.move()

    def distanceTo(self, object):
        x1, y1, z1 = self.position
        x2, y2, z2 = object.position
        return (((x2 - x1) ** 2) + ((y2 - y1) ** 2) + ((z2 - z1) ** 2)) ** (1 / 2)

    def lerp(self, frame1, frame2, alpha):
        x1, y1, z1 = frame1
        x2, y2, z2 = frame2
        x = x1 + (x2 - x1) * alpha
        y = y1 + (y2 - y1) * alpha
        z = z1 + (z2 - z1) * alpha
        return x, y, z

    def animate(self):
        for i in range(len(self.animation)):
            anim = self.animation[i]
            name = anim['name']
            if name == 'walk' and not self.walking:
                continue
            if name == 'hit' and not self.attacking:
                continue
            index = anim['index']
            origin = anim['origin']
            keyframes = anim['keyframes']
            rot = keyframes[math.floor((self.frames[i] / 10) % len(keyframes))]
            rotY = self.rotation[0]
            self.rotateSelfY(-rotY)
            self.rotateX(self.model[index], origin, rot[2])
            self.rotateSelfY(rotY)
            if self.frames[i] % (10 * len(keyframes)) == 10 * len(keyframes) - 1:
                if name == 'walk' and i == 1:
                    self.walking = False
                if name == 'hit':
                    self.attacking = False
            self.frames[i] += 1

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

    def rotateY(self, model, origin, theta):
        for part in model:
            for i in range(0, len(part.vertices), 3):
                ox = origin[0] + self.position[0]
                oz = origin[2] + self.position[2]
                x = ox + math.cos(theta) * (part.vertices[i] - ox) - math.sin(theta) * (part.vertices[i + 2] - oz)
                z = oz + math.sin(theta) * (part.vertices[i] - ox) + math.cos(theta) * (part.vertices[i + 2] - oz)
                part.vertices[i + 0] = x
                part.vertices[i + 2] = z

    def rotateSelfY(self, theta):
        for shape in self.model:
            for part in shape:
                for i in range(0, len(part.vertices), 3):
                    x = self.position[0] + math.cos(theta) * (part.vertices[i] - self.position[0]) - math.sin(theta) * (part.vertices[i + 2] - self.position[2])
                    z = self.position[2] + math.sin(theta) * (part.vertices[i] - self.position[0]) + math.cos(theta) * (part.vertices[i + 2] - self.position[2])
                    part.vertices[i] = x
                    part.vertices[i + 2] = z
        self.rotation = (self.rotation[0] + theta, self.rotation[1])
