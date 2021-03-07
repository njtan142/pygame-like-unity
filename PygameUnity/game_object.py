import pygame

pygame.init()


class GameObject:

    def __init__(self, name, x=0, y=0, z=0, layer=0):
        self.name = name
        self.children = {}
        self.transform = Transform(x, y, z)
        self.renderer = Renderer(layer)
        self.collider = None
        self.physics = None

    def add_component(self, component, params):
        if component == "image_renderer":
            self.renderer.image(params)
        if component == "text_renderer":
            self.renderer.text(params)
        if component == "collider":
            self.collider = Collider(params)
        if component == "physics":
            self.physics = Physics(params)

    def move(self, x, y, time_delta=1, collisions=None):
        if self.physics is not None:
            vx, vy = self.physics.movement(time_delta)
            x += vx
            y += vy

        x *= time_delta
        y *= time_delta

        self.msa(x, 0, time_delta, collisions)
        self.msa(0, y, time_delta, collisions)

    def msa(self, x, y, time_delta, collisions):
        self.transform.position.x += x
        self.transform.position.y += y

        if self.collider is None:
            return
        self.collider.left += x
        self.collider.top += y
        self.collider.update()
        if collisions is None:
            return
        for obj in collisions:
            if self.transform.position.z != collisions[obj].transform.position.z:
                continue
            if self.collider.colliderect(collisions[obj].collider):
                if x > 0:
                    self.collider.left = collisions[obj].collider.left - self.collider.width
                    self.collider.update()
                    if self.physics is not None:
                        if collisions[obj].physics is not None:
                            collisions[obj].physics.velocity.x += self.physics.velocity.x
                            self.physics.velocity.x = 0
                elif x < 0:
                    self.collider.left = collisions[obj].collider.right
                    self.collider.update()
                    if self.physics is not None:
                        if collisions[obj].physics is not None:
                            collisions[obj].physics.velocity.x += self.physics.velocity.x
                            self.physics.velocity.x = 0
                self.transform.position.x = self.collider.left + self.collider.width / 2

        for obj in collisions:
            if self.transform.position.z != collisions[obj].transform.position.z:
                continue
            if self.collider.colliderect(collisions[obj].collider):
                if y > 0:
                    self.collider.top = collisions[obj].collider.bottom
                    self.collider.update()
                    if self.physics is not None:
                        if collisions[obj].physics is not None:
                            if not collisions[obj].physics.rigidbody.is_kenimatic:
                                collisions[obj].physics.velocity.y += self.physics.velocity.y
                            self.physics.velocity.y = 0
                elif y < 0:
                    self.collider.top = collisions[obj].collider.top + self.collider.height
                    self.collider.update()
                    if self.physics is not None:
                        if collisions[obj].physics is not None:
                            if not collisions[obj].physics.rigidbody.is_kenimatic:
                                collisions[obj].physics.velocity.y += self.physics.velocity.y
                        self.physics.velocity.y = round(-self.physics.velocity.y * self.physics.material.bounciness)
                self.transform.position.y = self.collider.top - self.collider.height / 2

    def render(self, screen, x, y):
        screen.blit(self.renderer.to_render.surface,
                    (round(x - self.renderer.to_render.surface.get_width() / 2),
                     round(y - self.renderer.to_render.surface.get_height() / 2))
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
            if horizontal and vertical:
                return True
            if self.top == collision.top and self.bottom == collision.bottom:
                if self.right > collision.right > self.left:
                    return True
                if self.left < collision.left < self.right:
                    return True
            if self.left == collision.left and self.right == collision.right:
                if self.top > collision.top > self.bottom:
                    return True
                if self.bottom < collision.bottom < self.top:
                    return True
        collision_points = [(self.left, self.top),
                            (self.left, self.bottom),
                            (self.right, self.top),
                            (self.right, self.bottom)]
        for point in collision_points:
            horizontal = collision.left < point[0] < collision.right
            vertical = collision.top > point[1] > collision.bottom
            if horizontal and vertical:
                return True
        return False


class Physics:

    def __init__(self, params):
        self.velocity = Velocity()
        self.rigidbody = Rigidbody(params[0], params[1], params[2], params[3], params[4])
        self.material = Material()

    def movement(self, time_delta):
        x = self.velocity.x
        y = self.velocity.y
        if self.rigidbody.is_gravity:
            self.gravity(time_delta)
        return x, y

    def gravity(self, time_delta):
        self.velocity.y -= 9.81 * self.rigidbody.mass * time_delta


class Velocity:

    def __init__(self):
        self.x = 0
        self.y = 0


class Rigidbody:

    def __init__(self, mass, drag, angular_drag, use_gravity, is_kinematic):
        self.mass = mass
        self.drag = drag
        self.angular_drag = angular_drag
        self.is_gravity = use_gravity
        self.is_kenimatic = is_kinematic


class Material:

    def __init__(self, bounciness=0.3, friction=0.3):
        self.bounciness = bounciness
        self.friction = friction
