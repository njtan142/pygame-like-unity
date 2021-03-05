import pygame

pygame.init()


class GameObject:

    def __init__(self, name, x=0, y=0):
        self.name = name
        self.children = {}
        self.transform = Transform(x, y)
        self.renderer = Renderer()

    def add_component(self, component, params):
        if component == "image_renderer":
            self.renderer.image(params)
        if component == "text_renderer":
            self.renderer.text(params)

    def render(self, screen, x, y):
        # print(x, y)
        screen.blit(self.renderer.to_render.surface,
                    (x - self.renderer.to_render.surface.get_width() / 2,
                     y - self.renderer.to_render.surface.get_height() / 2)
                    )
    def add_child(self, child):
        self.children[child.name] = child


class Transform:

    def __init__(self, x, y):
        self.position = Position(x, y)
        print(self.position.x)


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Renderer:

    def __init__(self):
        pass

    def image(self, params):
        self.to_render = ImageRenderer(params)

    def text(self, params):
        self.to_render = TextRenderer(params)


class ImageRenderer:

    def __init__(self, params):
        self.surface = pygame.image.load(params[0]).convert_alpha()


class TextRenderer:

    def __init__(self, params):
        self.surface = params[0].render(params[1], params[2], params[3])


