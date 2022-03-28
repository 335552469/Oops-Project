
from re import T, X
from tkinter import Y
from turtle import width
import pygame, sys, random, time
pygame.init()

screenX, screenY = 500, 500
surface = pygame.display.set_mode((screenX, screenY))
blue = [0, 0, 255]
white = [255, 255, 255]
black = [0, 0, 0]

rate = 1


class Box:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.glowing = False
        self.end_color = white
        self.start_color = blue
        self.z = False
        self.cycle = False
    
    def draw(self):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0, 9)

    def glow(self):
        
        


box = Box(100, 100, 50, 50, blue)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if box.x <= mouse[0] <= box.x + box.width and box.y <= mouse[1] <= box.y + box.height:
                box.z = True
                
    
    box.glow()
    surface.fill(black)
    
    box.draw()

    pygame.display.update()
