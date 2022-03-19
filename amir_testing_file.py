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

    def __init__(self, x, y, width, height, order): # initialize some basic values of our boxes 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.order = order
        self.box_colour = (37,115,193)
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

    def glow(self,length):
        
        start_time = time.time()
        while True:
            time.sleep(0.01)
            current_color = self.interpolate_color(start_time,length,pygame.Color(255,255,255))
            self.box_colour = current_color
            self.draw_box(surface)
            pygame.display.flip()
            if start_time+length < time.time():
                break


class Sequence(object):
    def __init__(self, sequence, seq_amount):
        self.sequence = sequence
        if (seq_amount - len(self.sequence)) > 0:
            for i in range(seq_amount - len(self.sequence)):
                self.sequence.append([random.randint(0,2),random.randint(0,2)])

    def check_sequence(self, sequence):
        print(self.sequence,"should equal",sequence)
        if self.sequence == sequence:
            return True
        return False
    
    def reveal_sequence(self, cards, level):
        for i in self.sequence:
            cards[i[0]][i[1]].glow(1)


class Sound:
    def __init__(self):
        self.cardflip_sound = pygame.mixer.Sound("cardflip.wav")
        self.shuffle_sound = pygame.mixer.Sound("shuffle.wav")

    def cardflip(self):
        self.cardflip_sound.play()

    def shuffle(self):
        self.shuffle_sound.play()


box_matrix = [[Box((j)*137+53, (i)*137+53, 120, 120, [i,j]) for j in range(3)] for i in range(3)]
sequence_obtained = []
level_sequence = Sequence([[random.randint(1,2),random.randint(1,2)] for i in range(level)], 1)


print("Level",level,"| Winning Sequence: ",level_sequence.sequence)

soundboard = Sound()

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
                        soundboard.cardflip()
                        j.glow(1)
                        sequence_obtained.append(j.order)
        if len(sequence_obtained) == level:
            if level_sequence.check_sequence(sequence_obtained):
                print("you win")
                level += 1
            else:
                print("you lose")
                level = 1
                level_sequence = Sequence(level_sequence.sequence, level)
                print(level_sequence.sequence)
                level_sequence.reveal_sequence(box_matrix, level)
                
            sequence_obtained = []
            level_sequence = Sequence(level_sequence.sequence, level)
            level_sequence.reveal_sequence(box_matrix, level)
        
        
    pygame.display.update()