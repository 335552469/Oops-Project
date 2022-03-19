from msilib import sequence
from multiprocessing.connection import wait
import pygame, sys, random
pygame.init()

screenX, screenY = 500, 500
surface = pygame.display.set_mode((screenX, screenY))

run = True
clicks = 0
level = 0

# Isaak Makes a
class Box(object):

    def __init__(self, x, y, width, height, order): # innitialize some basic values of our boxes 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.order = order
        self.box_colour = [37,115,193]

    def draw_box(self, surface): # draws box
        pygame.draw.rect(surface, self.box_colour, (self.x, self.y, self.width, self.height), 0, 9)

    def mouse_detection(self, mouse):
        if mouse[0] >= self.x and mouse[0] <= self.x + self.width:
            if mouse[1] >= self.y and mouse[1] <= self.y + self.height:
                return True
        else:
            return False
    def glow(self):
        self.box_colour = [255, 255, 255]
    def unglow(self):
        self.box_colour = [37,115,193]


box_matrix = [[Box((j)*137+53, (i)*137+53, 120, 120, j) for j in range(3)] for i in range(3)]
sequence = []

def new_sequence():
    x = random.randint(0, 2)
    y = random.randint(0, 2)
    sequence.append((x, y))
    print(sequence)
    for i in range(len(sequence)):
        box_matrix[sequence[0]][sequence[1]].glow
    




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

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in box_matrix:
                for j in i:
                    if j.mouse_detection(pygame.mouse.get_pos()) == True:
                        j.glow()
                        clicks += 1

    if clicks == len(sequence):
        new_sequence()
        clicks = 0
        for i in box_matrix:
            for j in i:
                j.unglow()


    
    
    # box_matrix[0][0].glow()    
    pygame.display.update()

    