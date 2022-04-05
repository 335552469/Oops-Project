from msilib import sequence                 #
from multiprocessing.connection import wait # Imports
import pygame, sys, random, time, math      #
import threading

from pyrsistent import freeze
pygame.init()

screenX, screenY = 500, 500 # Dimensions of the game window
surface = pygame.display.set_mode((screenX, screenY))

run = True
play = 0 # 0 = Open screen, 1 = main game, 2 = death screen
correctClicks = 0
lose = False

global freezee
freezee = True

def thread(function):
    def fix(*x, **y):
        threading.Thread(target=function, args=x, kwargs=y).start()
    return fix

class Box(object):

    def __init__(self, x, y, width, height, order): # initializes values of the boxes 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.order = order
        self.boxColour = [37,115,193]
        self.defaultColor = self.boxColour

    def drawBox(self, surface): # draws a box
        pygame.draw.rect(surface, self.boxColour, (self.x, self.y, self.width, self.height), 0, 9)

    def mouseDetection(self, mouse):
        if mouse[0] >= self.x and mouse[0] <= self.x + self.width:
            if mouse[1] >= self.y and mouse[1] <= self.y + self.height: # Checks if the mouse is inside any given box and returns a boolean
                return True
        else:
            return False

    def interpolateColor(self, startTime, maxFadeTime, color): # Interpolates the fading of a given color based on the starting color,
                                                               # end color, and time.
        fract = (time.time() - startTime) / (maxFadeTime)
        if fract > 0.5:
            fract = 1 - fract * 1.3
        color1 = pygame.Color(*self.defaultColor)
        if fract < 0:
            return pygame.Color(*self.defaultColor)
        return color1.lerp(color, fract)

    @thread
    def glow(self,length,color,waitTime):
        global freezee
        time.sleep(waitTime)
        startTime = time.time() # Fades the color of a box in and out
        if color == pygame.Color(255,255,255): freezee = True
        for i in range(math.floor(length*100)):
            currentColor = self.interpolateColor(startTime,length,pygame.Color(color))
            self.boxColour = currentColor
            #self.drawBox(surface)
            #pygame.display.flip()
            time.sleep(0.01)
        freezee = False
        return 1354

    def freezeGlow(self,length,color,waitTime):
        time.sleep(waitTime)
        startTime = time.time() # Fades the color of a box in and out without threading
        for i in range(math.floor(length*100)):
            currentColor = self.interpolateColor(startTime,length,pygame.Color(color))
            self.boxColour = currentColor
            self.drawBox(surface)
            pygame.display.flip()
            time.sleep(0.01)

class HighScore:
    def __init__(self): # Initiates values for highscore
        self.score = 0

    def readScore(self):
        try:
            with open("highscore.txt", "r") as file: 
                self.score = str(file.readline()) # reads the "highscore.txt" file to see what the players highscore is
        except FileNotFoundError:
            print("No high score yet.") # Checks if the "highscore.txt" file exists

    def writeScore(self, score):
        with open("highscore.txt", "w") as file:
            file.write(str(score)) # updates the "highscore.txt" file with the players highscore

    def __str__(self):
        return f"The high score is {self.score}" # Text to present the highscore on the screen



class Sound:
    def __init__(self): # Initiates sounds
        self.cardflipSound = pygame.mixer.Sound("deep.mp3")
        self.shuffleSound = pygame.mixer.Sound("vine.mp3")

    def cardflip(self):
        self.cardflipSound.play() # Plays the sound the happens when a box is clicked

    @thread
    def shuffle(self):
        time.sleep(0.5)
        self.shuffleSound.play() # Plays the sound that happens at the beginning of each round

sound = Sound()

boxMatrix = [[Box((j)*137+53, (i)*137+53, 120, 120, j) for j in range(3)] for i in range(3)] # Creates the matrix for the 9 boxes
sequence = []

@thread
def newSequence(sequence,reset = False): # Controls the sequence of flashing boxes
    if reset:
        print("new sequence",sequence)
    print("curr sequence",sequence)
    x = random.randint(0, 2)
    y = random.randint(0, 2)
    sequence.append([x, y]) # adds a specific box into the sequence
    sound.shuffle() # plays the next round sound
    for i in range(len(sequence)):
        x = boxMatrix[sequence[i][0]][sequence[i][1]].glow(1 * (1 - 0.05 * len(sequence)),(255,255,255),i+1)



highScore = HighScore()

highScore.readScore()
score = 0
class Screen:
    def __init__(self, play, sequence, lose, correctClicks, score):
        self.play = play
        self.sequence = sequence
        self.lose = lose
        self.correctClicks = correctClicks
        self.score = score

    def start(self):
        while self.play == 0: # While loop for the opening screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # closes the game
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN: # checks if either the mouse has been pressed or if any key has been pressed
                    self.play = 1 # stops this while loop and starts the one for the main game
                
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

    def main(self):
        global freezee
        self.sequence = []
        newSequence(self.sequence, False)
        while self.play == 1: # While loop for the main game
            surface.fill((43 ,135 ,209)) # fills the screen a certain colour
            font = pygame.font.SysFont('Cooper', 30)
            write = font.render("HighScore: " + str(highScore.score) + "                               Level: " + str(self.score+1), True, (0, 0, 0))
            surface.blit(write, (55, 20)) # Writes the highscore and the level on the screen

            for i in boxMatrix:
                for j in i:
                    j.drawBox(surface) # draws the 9 boxes according to the box matrix

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # exits the game
                if event.type == pygame.MOUSEBUTTONDOWN: # Checks if the mouse has been pressed
                    for i in boxMatrix:
                        for j in i:
                            if freezee == False:
                                if j.mouseDetection(pygame.mouse.get_pos()) == True: # Checks if the mouse is in a box
                                    if j.x // 153 == self.sequence[self.correctClicks][1] and j.y // 153 == self.sequence[self.correctClicks][0]: # checks if the player has clicked on the correct box in the sequence
                                        sound.cardflip() # Plays the correct sound
                                        self.correctClicks += 1
                                        if self.correctClicks == len(self.sequence)-1:
                                            self.score +=1 # adds to the plaers score
                                        j.glow(0.5,(0,255,0),0) # makes the box glow white if the player has clicked the correct box
                                    else: # if the player correctClicks the wrong box
                                        if self.score >= int(highScore.score): # Checks if the player has beat their highscore
                                            highScore.score = str(self.score+1)
                                            highScore.writeScore(str(self.score+1)) # Adds the new highscore to the "highscore.txt" file
                                        
                                        j.freezeGlow(0.5,(255,0,0),0) # Makes the box glow red if the player has clicked the wrong box
                                        self.correctClicks = 0         #
                                        self.sequence = []              #
                                        self.score = 0                  # Resets correctClicks, the box sequence, the score, stops this while loop, and starts the lose screen while loop
                                        print("yuo loose dumbas")  #
                                        self.play = 2                   #
                                        break
                                        


            if self.correctClicks == len(self.sequence) and len(self.sequence) != 0 and self.play != 2: # checks if the player has completed the round
                print("LOST")
                newSequence(*self.sequence) # Starts the next round
                self.correctClicks = 0
            
            elif self.lose: # Checks if the player has lost
                newSequence(*self.sequence) # Starts the new round
                self.lose = False
                
            pygame.display.update() # Updates the screen

    def death(self):
        while self.play == 2: # While loop for the lose screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit() # closes the game
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.play = 1 # Stops this loop and starts the one for the main game


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
            self.lose = True

mainGame = Screen(play, sequence, lose, correctClicks, score)
while True:
    mainGame.start()
    mainGame.main()
    mainGame.death()