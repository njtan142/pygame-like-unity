import pygame

pygame.init()


class GameObject:

    def __init__(self, name, x=0, y=0, z=0, layer=0):
        self.name = name
        self.children = {}
        self.transform = Transform(x, y, z)
        self.renderer = Renderer(layer)
        self.collider = None

    def add_component(self, component, params):
        if component == "image_renderer":
            self.renderer.image(params)
        if component == "text_renderer":
            self.renderer.text(params)
        if component == "collider":
            self.collider = Collider(params)

    def move(self, x, y, collisions):
        self.transform.position.x += x
        self.transform.position.y += y

        if self.collider is None:
            return
        self.collider.left += x
        self.collider.top += y
        self.collider.update()
        for obj in collisions:
            if self.transform.position.z != collisions[obj].transform.position.z:
                continue
            if self.collider.colliderect(collisions[obj].collider):
                if x > 0:
                    self.collider.left = collisions[obj].collider.left - self.collider.width
                    self.collider.update()
                elif x < 0:
                    self.collider.left = collisions[obj].collider.right
                    self.collider.update()
                self.transform.position.x = self.collider.left + self.collider.width / 2

        for obj in collisions:
            if self.transform.position.z != collisions[obj].transform.position.z:
                continue
            if self.collider.colliderect(collisions[obj].collider):
                if y > 0:
                    self.collider.top = collisions[obj].collider.bottom
                    self.collider.update()
                elif y < 0:
                    self.collider.top = collisions[obj].collider.top + self.collider.height
                    self.collider.update()
                self.transform.position.y = self.collider.top - self.collider.height / 2

    def render(self, screen, x, y):
        # print(x, y)
        screen.blit(self.renderer.to_render.surface,
                    (x - self.renderer.to_render.surface.get_width() / 2,
                     y - self.renderer.to_render.surface.get_height() / 2)
                    )

    def add_child(self, child):
        self.children[child.name] = child


class Transform:

    def __init__(self, x, y, z):
        self.position = Position(x, y, z)


class Position:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Renderer:

    def __init__(self, layer):
        self.layer = layer

    def image(self, params):
        self.to_render = ImageRenderer(params)

    def text(self, params):
        self.to_render = TextRenderer(params)


class ImageRenderer:

    def __init__(self, params):
        self.surface = pygame.image.load(params).convert_alpha()


class TextRenderer:

    def __init__(self, params):
        self.surface = params[0].render(params[1], params[2], params[3])


class Collider:

    def __init__(self, params):
        self.left = params[0]
        self.top = params[1]
        self.width = params[2]
        self.height = params[3]
        self.right = params[0] + params[2]
        self.bottom = params[1] - params[3]
        print(self.left, self.top, self.right, self.bottom)

    def update(self):
        self.right = self.left + self.width
        self.bottom = self.top - self.height

    def colliderect(self, collision):
        if collision is None:
            return False
        if collision == self:
            return False
        collision_points = [(collision.left, collision.top),
                            (collision.left, collision.bottom),
                            (collision.right, collision.top),
                            (collision.right, collision.bottom)]
        for point in collision_points:
            horizontal = self.left < point[0] < self.right
            vertical = self.top > point[1] > self.bottom
            # print(vertical, self.top, point[1], self.bottom)
            # print(horizontal, vertical, horizontal and vertical)
            if horizontal and vertical:
                return True
        return False

