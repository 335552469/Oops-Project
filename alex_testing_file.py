import pygame, sys
pygame.init()

surface = pygame.display.set_mode((500, 500))

def draw_box():
    box = pygame.Surface((100, 100))
    fade = 0
    box.set_alpha(fade)
    surface.blit(box, (30, 30))

while True:
    surface.fill((43, 135, 209))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            draw_box()

    pygame.display.update()