import pygame
from game_object import GameObject

pygame.init()
container = GameObject("container")
test = GameObject("test")
container.add_child(test)
screen = pygame.display.set_mode((200, 200), pygame.FULLSCREEN|pygame.SCALED)
font = pygame.font.SysFont(None, 24)
test.add_component("text_renderer",
                   (font, "I love you", False, (255, 255, 255))
                   )

running = True
while running:


    test.render(screen, screen.get_width()/2, screen.get_height()/2)
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    pygame.display.flip()
