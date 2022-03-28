
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
<<<<<<< HEAD
        self.order = order
        self.box_colour = [37,115,193]
        self.default_color = self.box_colour

    def draw_box(self, surface): # draws box
        pygame.draw.rect(surface, self.box_colour, (self.x, self.y, self.width, self.height), 0, 9)

    def mouse_detection(self, mouse):
        if mouse[0] >= self.x and mouse[0] <= self.x + self.width:
            if mouse[1] >= self.y and mouse[1] <= self.y + self.height:
                return True
        else:
            return False

    def interpolate_color(self, start_time, max_fade_time, color):
        fract = (time.time() - start_time) / (max_fade_time)
        if fract > 0.5:
            fract = 1 - fract * 1.3
        color1 = pygame.Color(*self.default_color)
        if fract < 0:
            return pygame.Color(*self.default_color)
        return color1.lerp(color, fract)
        
    def glow(self,length,color):
        start_time = time.time()
        while True:
            time.sleep(0.01)
            current_color = self.interpolate_color(start_time,length,pygame.Color(color))
            self.box_colour = current_color
            self.draw_box(surface)
            pygame.display.flip()
            if start_time+length < time.time():
                break

class HighScore:
    def __init__(self):
        self.score = 0

    def read_score(self):
        try:
            with open("highscore.txt", "r") as file:
                self.score = str(file.readline())
        except FileNotFoundError:
            print("No high score yet.")

    def write_score(self, score):
        with open("highscore.txt", "w") as file:
            file.write(str(score))

    def __str__(self):
        return f"The high score is {self.score}"


class Sound:
    def __init__(self):
        self.cardflip_sound = pygame.mixer.Sound("cardflip.wav")
        self.shuffle_sound = pygame.mixer.Sound("shuffle.wav")

    def cardflip(self):
        self.cardflip_sound.play()

    def shuffle(self):
        self.shuffle_sound.play()

sound = Sound()

box_matrix = [[Box((j)*137+53, (i)*137+53, 120, 120, j) for j in range(3)] for i in range(3)]
sequence = []

def new_sequence():
    x = random.randint(0, 2)
    y = random.randint(0, 2)
    sequence.append([x, y])
    sound.shuffle()

    for i in sequence:
        box_matrix[i[0]][i[1]].glow(1,(255,255,255))

=======
        self.color = color

        self.glowing = False
        self.end_color = white
        self.start_color = blue
        self.z = False
        self.cycle = False
    
    def draw(self):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0, 9)

    def glow(self):
        
<<<<<<< HEAD
        
=======
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
               
>>>>>>> f3479888bb57c4a184be6a0471c1fd4021746ded
>>>>>>> ff70f55a332cef1005db9af154b85d7efd89e845


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
