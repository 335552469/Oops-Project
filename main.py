import pygame as pg
#ball
pg.init()

surface = pg.display.set_mode((500, 500))
run = True
# pepee
class Box(object):
    def __init__(self):
        pass 

    def draw_box(self):
        pass
    def glow(self):
        print("hello world")
    

while run: 
    for event in pg.event.get():
        if event.type == pg.QUIT: 
            run = False

    surface.fill((23, 85, 255))


    pg.display.update()
            
