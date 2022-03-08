import pygame, sys
pygame.init()

surface = pygame.display.set_mode((500, 500))

run = True

class Box(object):

    def __init__(self, x, y, width, height, order): # innitialize some basic values of our boxes 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.order = order

    def draw_box(self, surface): # draws box
        pygame.draw.rect(surface, (37,115,193), (self.x, self.y, self.width, self.height), 0, 5)
    def glow(self): # this isnt manditory but I wanted this to be the affect that happens when the mouse hovers over the box
        pass

box_matrix = [[Box((j)*130 + 60, (i)*130 + 60, 120, 120, j) for j in range(3)] for i in range(3)]
while True:
    surface.fill((43 ,135 ,209))

    for i in box_matrix:
        for j in i:
            j.draw_box(surface)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
    pygame.display.update()