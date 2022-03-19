from msilib import sequence
from multiprocessing.connection import wait
import pygame, sys, random, time
pygame.init()

screenX, screenY = 500, 500
surface = pygame.display.set_mode((screenX, screenY))

run = True
clicks = 0

class Box(object):

    def __init__(self, x, y, width, height, order): # innitialize some basic values of our boxes 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
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


highscore = HighScore()

highscore.read_score()

while True:
    surface.fill((43 ,135 ,209))
    font = pygame.font.SysFont('Cooper', 40)
    write = font.render("Score: " + str(highscore.score), False, (0, 0, 0))
    surface.blit(write, (55, 15)) 

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
                        xpos = j.x // 153
                        ypos = j.y // 153
                        print(sequence)
                        print(clicks)
                        if xpos == sequence[clicks][1] and ypos == sequence[clicks][0]:
                            sound.cardflip()
                            j.glow(1,(255,255,255))
                            clicks += 1
                        else:
                            j.glow(1,(255,0,0))
                            clicks = 0
                            sequence = []
                            print("you loose dumbas")
                            new_sequence()

    if clicks == len(sequence):
        new_sequence()
        clicks = 0 
    pygame.display.update()