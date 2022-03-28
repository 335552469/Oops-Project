
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
        print(self.color, end=" ")
        print(self.end_color)
        
        if self.z == True:
            for i in range(3):
                if not self.cycle:
                    if self.color[i] != self.end_color[i]:
                        
                        if self.color[i] >= self.end_color[i]:
                            self.color[i] -= rate
                        elif self.color[i] <= self.end_color[i]:
                            
                            self.color[i] += rate
                        
                        if self.color == self.end_color:
                            self.cycle = True
                else:
                    if self.color[i] != self.start_color[i]:
                        if self.color[i] >= self.start_color[i]:
                            self.color[i] -= rate
                        elif self.color[i] <= self.start_color[i]:
                            self.color[i] += rate
                        else:
                            if self.color == self.start_color:
                                self.cycle = False
                                self.z = False
               


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
