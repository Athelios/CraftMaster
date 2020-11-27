from creature import Creature
import math

class Npc(Creature):
    def __init__(self, world, position, health, dy=0, walkSpeed=5, flying=False, flySpeed=10, height=1, jumpHeight=1.0):
        self.world = world
        super(Npc, self).__init__(position, health, dy, walkSpeed, flying, flySpeed, height, jumpHeight)
