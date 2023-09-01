import pygame
from pygame import gfxdraw

def render_ellipse(r1:int, r2:int, color, antialias:bool = True):
    color = pygame.Color(color)
    main_surf = pygame.Surface([r1*2+1, r2*2+1], pygame.SRCALPHA, 32)

    if antialias:
        gfxdraw.aaellipse(main_surf, r1, r2, r1, r2, color)
    gfxdraw.filled_ellipse(main_surf, r1, r2, r1, r2, color)

    return main_surf

def instant_ellipse(surface:pygame.Surface, center, r1:int, r2:int, color, antialias:bool = True):
    main_surf = render_ellipse(r1, r2, color, antialias)
    surface.blit(main_surf, [x-y for x, y in zip(center, [r1, r2])])


win = pygame.display.set_mode((800, 500))

s = render_ellipse(20, 20, "blue")
s1 = s

while True:
    events = pygame.event.get()
    mpos = pygame.mouse.get_pos()
    mprd = pygame.mouse.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()

    win.fill("white")

    win.blit(s, (100, 100))
    win.blit(s1, (100, 100))

    pygame.display.update()
