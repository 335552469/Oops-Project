from msilib import sequence                 #
from multiprocessing.connection import wait # Imports
import pygame, sys, random, time            #
pygame.init()

screenX, screenY = 500, 500 # Dimensions of the game window
surface = pygame.display.set_mode((screenX, screenY))

run = True
play = 0 # 0 = Open screen, 1 = main game, 2 = death screen
correct_clicks = 0
lose = False

class Box(object):

    def __init__(self, x, y, width, height, order): # innitializes values of the boxes 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.order = order
        self.box_colour = [37,115,193]
        self.default_color = self.box_colour

    def draw_box(self, surface): # draws a box
        pygame.draw.rect(surface, self.box_colour, (self.x, self.y, self.width, self.height), 0, 9)

    def mouse_detection(self, mouse):
        if mouse[0] >= self.x and mouse[0] <= self.x + self.width:
            if mouse[1] >= self.y and mouse[1] <= self.y + self.height: # Checks if the mouse is inside any given box and returns a boolean
                return True
        else:
            return False

    def interpolate_color(self, start_time, max_fade_time, color): # Interpolates the fading of a given color based on the starting color,
                                                                   # end color, and time.
        fract = (time.time() - start_time) / (max_fade_time)
        if fract > 0.5:
            fract = 1 - fract * 1.3
        color1 = pygame.Color(*self.default_color)
        if fract < 0:
            return pygame.Color(*self.default_color)
        return color1.lerp(color, fract)

    def glow(self,length,color):
        start_time = time.time() # Fades the color of a box in and out
        while True:
            time.sleep(0.01)
            current_color = self.interpolate_color(start_time,length,pygame.Color(color))
            self.box_colour = current_color
            self.draw_box(surface)
            pygame.display.flip()
            if start_time+length < time.time():
                break

class HighScore:
    def __init__(self): # Initiates values for highscore
        self.score = 0

    def read_score(self):
        try:
            with open("highscore.txt", "r") as file: 
                self.score = str(file.readline()) # reads the "highscore.txt" file to see what the players highscore is
        except FileNotFoundError:
            print("No high score yet.") # Checks if the "highscore.txt" file exists

    def write_score(self, score):
        with open("highscore.txt", "w") as file:
            file.write(str(score)) # updates the "highscore.txt" file with the players highscore

    def __str__(self):
        return f"The high score is {self.score}" # Text to present the highscore on the screen


class Sound:
    def __init__(self): # Initiates sounds
        self.cardflip_sound = pygame.mixer.Sound("deep.mp3")
        self.shuffle_sound = pygame.mixer.Sound("vine.mp3")

    def cardflip(self):
        self.cardflip_sound.play() # Plays the sound the happens when a box is clicked

    def shuffle(self):
        self.shuffle_sound.play() # Plays the sound that happens at the beginning of each round

sound = Sound()

box_matrix = [[Box((j)*137+53, (i)*137+53, 120, 120, j) for j in range(3)] for i in range(3)] # Creates the matrix for the 9 boxes
sequence = []

def new_sequence(): # Controls the sequence of flashing boxes
    x = random.randint(0, 2)
    y = random.randint(0, 2)
    sequence.append([x, y]) # adds a specific box into the sequence
    sound.shuffle() # plays the next round sound

    for i in sequence:
        box_matrix[i[0]][i[1]].glow(1,(255,255,255)) # makes the random box in the sequence glow 


highscore = HighScore()

highscore.read_score()
score = 0

while play == 0: # While loop for the opening screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit() # closes the game
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN: # checks if either the mouse has been pressed or if any key has been pressed
            play = 1 # stops this while loop and starts the one for the main game
        
    surface.fill((43 ,135 ,209)) # makes the background a certain colour
    font = pygame.font.SysFont('Cooper', 50)
    write = font.render("Sequence Memory Test", True, (255, 255, 255))
    surface.blit(write, (55, 230)) # Writes "Sequence Memory Test" on the screen

    font = pygame.font.SysFont('Cooper', 30)
    write = font.render("Memorize the pattern", True, (255, 255, 255))
    surface.blit(write, (140, 265)) # Writes "Memorize the pattern" on the screen

    font = pygame.font.SysFont('Cooper', 40)
    write = font.render("Press any key to begin", True, (255, 255, 255))
    surface.blit(write, (105, 310))  # Writes "Press any key to begin" on the screen

    pygame.draw.rect(surface, (255, 255, 255), (190, 75 , 50 , 50), 0, 9)  #
    pygame.draw.rect(surface, (255, 255, 255), (250, 75 , 50 , 50), 0, 9)  #
                                                                           # 
    pygame.draw.rect(surface, (255, 255, 255), (190, 135 , 50 , 50), 0, 9) # Draws the 4 squares at the top of the screen
    pygame.draw.rect(surface, (255, 255, 255), (250, 135 , 50 , 50), 0, 9) #
                                                                           #
    pygame.draw.rect(surface, (43, 135, 209), (257, 143, 35 , 35), 0, 9)   #

    pygame.display.update() # Updates the screen


while play == 1: # While loop for the main game
    surface.fill((43 ,135 ,209)) # fills the screen a certain colour
    font = pygame.font.SysFont('Cooper', 30)
    write = font.render("HighScore: " + str(highscore.score) + "                               Level: " + str(score+1), True, (0, 0, 0))
    surface.blit(write, (55, 20)) # Writes the highscore and the level on the screen

    for i in box_matrix:
        for j in i:
            j.draw_box(surface) # draws the 9 boxes according to the box matrix

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit() # exits the game
        if event.type == pygame.MOUSEBUTTONDOWN: # Checks if the mouse has been pressed
            for i in box_matrix:
                for j in i:
                    if j.mouse_detection(pygame.mouse.get_pos()) == True: # Checks if the mouse is in a box
                        if j.x // 153 == sequence[correct_clicks][1] and j.y // 153 == sequence[correct_clicks][0]: # checks if the player has clicked on the correct box in the sequence
                            sound.cardflip() # Plays the correct sound
                            correct_clicks += 1
                            if correct_clicks == len(sequence)-1:
                                score +=1 # adds to the plaers score
                            j.glow(0.5,(0,255,0)) # makes the box glow white if the player has clicked the correct box
                        else: # if the player correct_clicks the wrong box
                            if score >= int(highscore.score): # Checks if the player has beat their highscore
                                highscore.score = str(score+1)
                                highscore.write_score(str(score+1)) # Adds the new highscore to the "highscore.txt" file
                               
                            j.glow(0.5,(255,0,0)) # Makes the box glow red if the player has clicked the wrong box
                            correct_clicks = 0         #
                            sequence = []              #
                            score = 0                  # Resets correct_clicks, the box sequence, the score, stops this while loop, and starts the lose screen while loop
                            print("yuo loose dumbas")  #
                            play = 2                   #
                            break
                            


    if correct_clicks == len(sequence) and play != 2: # checks if the player has completed the round
        new_sequence() # Starts the next round
        correct_clicks = 0
    
    if lose: # Checks if the player has lost
        new_sequence() # Starts the new round
        lose = False
        
    pygame.display.update() # Updates the screen

while play == 2: # While loop for the lose screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit() # closes the game
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            play = 1 # Stops this loop and starts the one for the main game


    surface.fill((43 ,135 ,209)) # Fills the creen a certain colour

    font = pygame.font.SysFont('Cooper', 50)
    write = font.render("Sequence Memory Test", True, (255, 255, 255))
    surface.blit(write, (55, 230)) # Writes "Sequence Memory Test" on the screen

    font = pygame.font.SysFont('Cooper', 30)
    write = font.render("Press any key to try again.", True, (255, 255, 255))
    surface.blit(write, (120, 300)) # Writes "Press any key to try again." on the screen
    
    pygame.draw.rect(surface, (255, 255, 255), (190, 75 , 50 , 50), 0, 9)  #
    pygame.draw.rect(surface, (255, 255, 255), (250, 75 , 50 , 50), 0, 9)  #
                                                                           #
    pygame.draw.rect(surface, (255, 255, 255), (190, 135 , 50 , 50), 0, 9) # Draws the 4 squares at the top of the screen
    pygame.draw.rect(surface, (255, 255, 255), (250, 135 , 50 , 50), 0, 9) #
                                                                           #
    pygame.draw.rect(surface, (43, 135, 209), (257, 143, 35 , 35), 0, 9)   #

    pygame.display.update() # Updates the screen
    lose = True
