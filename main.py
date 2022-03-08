import pygame as pg
pg.init()

surface = pg.display.set_mode((500, 500))
run = True

# The box class should be a class that draws a box for each point in the matrix
class Box(object):

    def __init__(self): # innitialize some basic values of our boxes 
        pass 

    def draw_box(self): # draws box
        pass

    def glow(self): # this isnt manditory but I wanted this to be the affect that happens when the mouse hovers over the box
        pass

# We inherit the box into the box matrix class in order to mess with it from within the function
class Matrix(Box):
    def __init__(self): # if you dont remember class inheritence this is some basic syntax, if you would like to change it go ahead.
        super().__init__()
    
    # This method will populate the 2D list with initial values (not manditory, possible to do outside of the class, class will just take matrix as a parameter)
    def populate(self):
        pass
    
    # Most important method. Used to increase the size of the list going from a (3x3) list to a (4x4) to (5x5).... or however it increases online (check website for details)
    # Note: Dont make it increase on win, we will do that in the main code in order to keep our classes organized and on topic
    def get_bigger(self):
        pass

# ONLY MANDITORY VARIABLE SHOULD BE A 2D 3x3 MATRIX
matrix = [[0 for j in range(3)] for i in range(3)] # --> this just makes a matrix of 3x3 zeros using list comprehension, change it to your hearts content based on the coding process

while run: 
    for event in pg.event.get():
        if event.type == pg.QUIT: 
            run = False

    surface.fill((23, 85, 255))


    pg.display.update()
            
