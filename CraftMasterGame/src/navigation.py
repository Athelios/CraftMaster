import math

def normalize(position):
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return x, y, z

class Node:
    def __init__(self, position, neighbours=None):
        if neighbours is None:
            neighbours = []
        self.position = position
        self.neighbours = neighbours
        self.visited = False

    def distance(self, node):
        x1, y1, z1 = self.position
        x2, y2, z2 = node.position
        return (((x2-x1)**2)+((y2-y1)**2)+((z2-z1)**2))**(1/2)

class Graph:
    def __init__(self, start, end):
        self.start = Node(start)
        self.end = Node(end)
        self.nodes = {self.start.position: self.start}
        self.discoverable = {self.start.position: self.start}
        self.path = None
        self.steps = 0

    def nearest(self):
        nearest = list(self.discoverable.values())[0]
        dist = self.end.distance(nearest)
        for node in self.discoverable.values():
            d = self.end.distance(node)
            if d < dist:
                dist = d
                nearest = node
        return nearest

    def step(self, last, walkable):
        origin = self.discoverable.pop(last.position)
        for pos in walkable:
            if pos not in self.discoverable:
                if pos not in self.nodes:
                    node = Node(pos, [origin])
                    self.discoverable[pos] = node
                    self.nodes[pos] = node
                    if node not in origin.neighbours:
                        origin.neighbours.append(node)
            else:
                node = self.discoverable[pos]
                if origin not in node.neighbours:
                    node.neighbours.append(origin)
                if node not in origin.neighbours:
                    origin.neighbours.append(node)
        if self.end.position in walkable:
            self.path = self.find_path()
        self.steps += 1

    def find_path(self):
        queue = [[self.start]]
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if not node.visited:
                for neighbour in node.neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    if neighbour.position == self.end.position:
                        return new_path
                node.visited = True

class Navigation:
    def __init__(self, npc):
        self.npc = npc
        self.world = npc.world
        self.graph = None
        self.path = None
        self.shift = 0.0

    def navigate(self):
        start = normalize(self.npc.position)
        end = normalize(self.npc.goal)
        self.graph = Graph(start, end)
        self.shift = 0.0
        while not self.graph.path and self.graph.steps < self.npc.SEEK_MAX and self.graph.discoverable:
            nearest = self.graph.nearest()
            walkable = self.world.walkable(nearest.position)
            self.graph.step(nearest, walkable)
        self.path = self.graph.path

    def interpolate(self, pos1, pos2, alpha):
        x1, y1, z1 = pos1
        x2, y2, z2 = pos2
        x = x1 + (x2 - x1) * alpha
        y = y1 + (y2 - y1) * alpha
        z = z1 + (z2 - z1) * alpha
        return x, y, z

    def move(self):
        if self.path:
            pos1 = self.path[math.floor(self.shift)].position
            pos2 = self.path[math.ceil(self.shift)].position
            pos = self.interpolate(pos1, pos2, self.shift % 1)
            if self.shift + 0.05 >= len(self.path) - 1:
                self.npc.goal = None
            else:
                self.shift += 0.05
            pos = (pos[0], pos[1] - 0.25, pos[2])
            return pos
        else:
            return self.npc.position
