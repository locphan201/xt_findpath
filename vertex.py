class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.connected_to = []

    def connect(self, other):
        self.connected_to.append(other)

    def disconnect(self, vertex):
        self.connected_to.remove(vertex)