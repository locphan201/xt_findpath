import pygame as pg
from vertex import Vertex

def read_file():
    vertices = []
    try:
        with open('data.txt', 'r') as file:
            lines = file.readlines()

        setup = True
        for line in lines:
            if setup:
                if line == '-\n':
                    setup = False
                else:
                    line = line.strip().split(' ')
                    vertices.append(Vertex(int(line[0]), int(line[1])))
            else:
                if line == 'end':
                    break
                else:
                    line = line.strip().split('-')
                    v1, v2 = int(line[0]), int(line[1])
                    vertices[v1].connect(v2)
                    vertices[v2].connect(v1)
    except:
        print('Cannot find the text file!')
    return vertices

def findPath(root, target, vertices):
    visited = [False] * len(vertices)
    path = []
    return findPathHelper(root, target, vertices, visited, path)[1]

def findPathHelper(root, target, vertices, visited, path):
    visited[root] = True
    path.append(root)
    if root == target:
        return True, path
    for i in vertices[root].connected_to:
        if not visited[i]:
            if findPathHelper(i, target, vertices, visited, path)[0]:
                return True, path
    path.pop()
    return False, path

class Path:
    def __init__(self, img_file):
        pg.init()
        self.img = pg.image.load(img_file)
        width, height = self.img.get_width(), self.img.get_height()
        self.screen = pg.display.set_mode((width, height))
        self.fps = 32
        self.clock = pg.time.Clock()
        self.running = True

        ######################
        self.vertices = read_file()
        self.connections = []
        ######################

    def draw(self):
        self.screen.blit(self.img, (0, 0))
        c, v = self.connections, self.vertices
        if len(c) >= 2:
            for i in range(0, len(c) - 1):
                pg.draw.line(self.screen, (250, 253, 15), (v[c[i]].x, v[c[i]].y), (v[c[i+1]].x, v[c[i+1]].y), 5)

        for i in range(len(v)):
            if i in c:
                pg.draw.circle(self.screen, (0, 0, 0), (v[i].x, v[i].y), 10)
                pg.draw.circle(self.screen, (255, 0, 0), (v[i].x, v[i].y), 10, 3)
            else:
                pg.draw.circle(self.screen, (0, 0, 255), (v[i].x, v[i].y), 10)
                pg.draw.circle(self.screen, (0, 0, 0), (v[i].x, v[i].y), 10, 3)

    def events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

            if e.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                for i in range(len(self.vertices)):
                    if abs(self.vertices[i].x - x) <= 10:
                        if abs(self.vertices[i].y - y) <= 10:
                            if not i in self.connections:
                                if len(self.connections) == 0:
                                    self.connections.append(i)
                                else:
                                    self.connections = findPath(self.connections[0], i, self.vertices)

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE:
                    self.connections = []

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.events()
            self.draw()
            pg.display.update()
        pg.quit()