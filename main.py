import pygame
from game_object import GameObject
from camera import Camera

pygame.init()
screen = pygame.display.set_mode((200, 200), pygame.FULLSCREEN | pygame.SCALED)
container = GameObject("container")
test = GameObject("test")
container.add_child(test)
camera = Camera(screen.get_width(), screen.get_height(), container.children)
font = pygame.font.SysFont(None, 24)
test.add_component("text_renderer",
                   (font, "I love you", False, (255, 255, 255))
                   )

running = True
while running:
    screen.fill((0, 20, 0))
    camera.render(screen)
    # test.transform.position.y += 0.1
    # camera.game_object.transform.position.y += 0.1
    # print(test.transform.position.y, camera.game_object.transform.position.y)
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_w:
                camera.game_object.transform.position.y += 20
            if event.key == pygame.K_s:
                camera.game_object.transform.position.y -= 20


    pygame.display.flip()
