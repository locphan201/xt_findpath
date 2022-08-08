import pygame as pg

class MapSetup:
    def __init__(self, img_file):
        pg.init()
        self.img = pg.image.load(img_file)
        width, height = self.img.get_width(), self.img.get_height()
        self.screen = pg.display.set_mode((width, height))
        self.fps = 32
        self.clock = pg.time.Clock()
        self.running = True

        ######################
        self.vertices = []
        self.connection = []
        self.selected = [False]
        ######################

    def draw(self):
        self.screen.blit(self.img, (0, 0))
        font = pg.font.SysFont('Arial', 25)
        if self.selected[0]:
            text_surface = font.render('Lines/Connections', False, (0, 0, 0))
        else:
            text_surface = font.render('Points/Intersections', False, (0, 0, 0))
        self.screen.blit(text_surface, (0, 0))

        if self.selected[0] and len(self.selected) == 2:
            i = self.selected[1]
            x, y = pg.mouse.get_pos()
            pg.draw.line(self.screen, (  0,   0,  0), (self.vertices[i][0], self.vertices[i][1]), (x, y), 9)
            pg.draw.line(self.screen, (250, 253, 15), (self.vertices[i][0], self.vertices[i][1]), (x, y), 3)

        for l in self.connection:
            pg.draw.line(self.screen, (0, 0, 0), (self.vertices[l[0]][0], self.vertices[l[0]][1]), (self.vertices[l[1]][0], self.vertices[l[1]][1]), 9)

        for i in range(len(self.vertices)):
            if self.selected[0] and len(self.selected) == 2 and self.selected[1] == i:
                pg.draw.circle(self.screen, (0, 0, 0), (self.vertices[i][0], self.vertices[i][1]), 10)
                pg.draw.circle(self.screen, (180, 0, 0), (self.vertices[i][0], self.vertices[i][1]), 10, 3)
            else:
                pg.draw.circle(self.screen, (0, 0, 180), (self.vertices[i][0], self.vertices[i][1]), 10)
                pg.draw.circle(self.screen, (0, 0,   0), (self.vertices[i][0], self.vertices[i][1]), 10, 3)


    def events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                with open('data.txt', 'w') as file:
                    for v in self.vertices:
                        file.write(str(v[0]) + ' ' + str(v[1]) + '\n')
                    file.write('-\n')
                    for c in self.connection:
                        file.write(str(c[0]) + '-' + str(c[1]) + '\n')
                    file.write('end')
                self.running = False

            if e.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                if self.selected[0]:
                    for i in range(len(self.vertices)):
                        if abs(self.vertices[i][0] - x) <= 25:
                            if abs(self.vertices[i][1] - y) <= 25:
                                if len(self.selected) == 1:
                                    self.selected.append(i)
                                elif len(self.selected) == 2:
                                    if not self.selected[1] == i:
                                        if not (self.selected[1], i) in self.connection and not (i, self.selected[1]) in self.connection:
                                            self.connection.append((self.selected[1], i))
                                            self.selected = [True]
                else:
                    exist = False
                    for i in range(len(self.vertices)):
                        if abs(self.vertices[i][0] - x) <= 25:
                            if abs(self.vertices[i][1] - y) <= 25:
                                exist = True
                    if not exist:
                        self.vertices.append((x, y))

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE:
                    self.selected[0] = not self.selected[0]

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.events()
            self.draw()
            pg.display.update()
        pg.quit()

