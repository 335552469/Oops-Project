import pygame as pg
pg.init()

surface = pg.display.set_mode((500, 500))
run = True
# comment 1
class Box(object):
    def __init__(self):
        pass 

    def draw_box(self):
        pass
    def glow(self):
        pass
    

while run: 
    for event in pg.event.get():
        if event.type == pg.QUIT: 
            run = False

    surface.fill((23, 85, 255))


    pg.display.update()
            
