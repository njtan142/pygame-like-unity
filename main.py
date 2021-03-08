import pygame
from PygameUnity.game_object import GameObject
from camera import Camera
from datetime import datetime as dt
from Collision import Collision

pygame.init()
screen = pygame.display.set_mode((800, 800))
container = GameObject("container")
test = GameObject("test", -400, 0, 0, -1)
test2 = GameObject("test2", 10, 40, 0, -1)
test3 = GameObject('test3', 10, 100, 0, -1)
container.add_child(test)
container.add_child(test2)
container.add_child(test3)
camera = Camera(screen.get_width(), screen.get_height(), container.children)
font = pygame.font.SysFont(None, 24)
test.add_component("image_renderer",
                   "assets/block.png"
                   )
test.add_component("collider",
                   (test.transform.position.x - test.renderer.to_render.surface.get_width() / 2,
                    test.transform.position.y + test.renderer.to_render.surface.get_height() / 2,
                    test.renderer.to_render.surface.get_width() * 100,
                    test.renderer.to_render.surface.get_height())
                   )
test2.add_component("image_renderer",
                    "assets/block.png"
                    )
test2.add_component("collider",
                    (test2.transform.position.x - test2.renderer.to_render.surface.get_width() / 2,
                     test2.transform.position.y + test2.renderer.to_render.surface.get_height() / 2,
                     test2.renderer.to_render.surface.get_width(),
                     test2.renderer.to_render.surface.get_height())
                    )
test2.add_component("physics",
                    (20, 0, 0.005, True, False)
                    )
test3.add_component("image_renderer",
                    "assets/block.png"
                    )
test3.add_component("collider",
                    (test3.transform.position.x - test3.renderer.to_render.surface.get_width() / 2,
                     test3.transform.position.y + test3.renderer.to_render.surface.get_height() / 2,
                     test3.renderer.to_render.surface.get_width(),
                     test3.renderer.to_render.surface.get_height())
                    )
test3.add_component("physics",
                    (20, 0, 0.005, True, False)
                    )
test.add_component("physics",
                   (20, 0, 0.005, False, True))

polygon = Collision(
    [
    (-16, 16),
     # (16, 16),
     (16, -16),
     (-16, -16)], pygame
)
nope = Collision(
    [
    # (-16, 16),
     (16, 16),
     (16, -16),
     (-16, -16)], pygame
)
print(polygon.origin)
camera.target = test2
running = True


def pygame_events():
    global running
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                test2.physics.velocity.y = 300
        if event.type == pygame.MOUSEBUTTONDOWN:
            polygon.multiple_collision([(pygame.mouse.get_pos()[0] - screen.get_width()/2,
                                     -pygame.mouse.get_pos()[1] + screen.get_height()/2)])


current_time_dt = dt.now()
current_time_ts = dt.timestamp(current_time_dt)
last_time_dt = dt.now()
last_time_ts = dt.timestamp(last_time_dt)
time_count = 0
time_delta = 0.016  # 1/60 of a second
time_scale = 1
while running:
    screen.fill((0, 20, 0))

    key_state = pygame.key.get_pressed()
    horizontal = key_state[pygame.K_d] - key_state[pygame.K_a]
    vertical = key_state[pygame.K_s] - key_state[pygame.K_w]
    # test.transform.position.y += 0.1
    # camera.game_object.transform.position.y += 0.1
    # print(test.transform.position.y, camera.game_object.transform.position.y)
    test2.move(0, 0, time_delta, container.children)
    test3.move(0, 0, time_delta, container.children)
    test.move(0, 0, time_delta, container.children)
    polygon.move(horizontal * 100 * time_delta, -vertical * 100 * time_delta)
    pygame_events()
    camera.movement(time_delta)
    camera.render(screen)
    polygon.draw_lines(screen)
    nope.draw_lines(screen)
    pygame.display.flip()

    last_time_dt = dt.now()
    last_time_ts = dt.timestamp(last_time_dt)
    time_delta = last_time_ts - current_time_ts
    time_count += time_delta
    current_time_dt = dt.now()
    current_time_ts = dt.timestamp(current_time_dt)

    if time_count >= 1:
        polygon.calculate_origin()
        time_count -= 1
