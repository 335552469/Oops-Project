from msilib import sequence
import pygame, sys, random, time
pygame.init()


screenX, screenY = 500, 500
surface = pygame.display.set_mode((screenX, screenY))

run = True
level = 1

#TODO: function to fade boxes in/out
#TODO: sequences function to create a new round

class Box(object):

    def __init__(self, x, y, width, height, order): # innitialize some basic values of our boxes 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.order = order
        self.box_colour = (37,115,193)

    def draw_box(self, surface): # draws box
        pygame.draw.rect(surface, self.box_colour, (self.x, self.y, self.width, self.height), 0, 9)

    def mouse_detection(self, mouse):
        if mouse[0] >= self.x and mouse[0] <= self.x + self.width:
            if mouse[1] >= self.y and mouse[1] <= self.y + self.height:
                return True
        else:
            return False
    def glow(self):
        pass


class Sequence(object):
    def __init__(self, seq_amount):
        self.sequence = [[random.randint(1,2),random.randint(1,2)] for i in range(seq_amount)]

    def check_sequence(self, sequence):
        if self.sequence == sequence:
            return True
        return False
    
    def reveal_sequence(self, cards, level):
        for i in cards:
            for j in i:
                i.glow()
                time.sleep(2/(level)*1.2)

    

test = Sequence(5)

box_matrix = [[Box((j)*137+53, (i)*137+53, 120, 120, [j,i]) for j in range(3)] for i in range(3)]
sequence_obtained = []
level_sequence = Sequence(level)


print("Level",level,"| Winning Sequence: ",level_sequence.sequence)


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
                        sequence_obtained.append(j.order)
                        print(sequence_obtained)
                        print(level, len(sequence_obtained))
        if len(sequence_obtained) == level:
            if level_sequence.check_sequence(sequence_obtained):
                print("you win")
                level += 1
            else:
                print("you lose")
            sequence_obtained = []
            level_sequence = Sequence(level)
            level_sequence.reveal(box_matrix, level)
        
        
    pygame.display.update()