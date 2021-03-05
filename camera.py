from game_object import GameObject


class Camera:

    def __init__(self, width, height, game_objects):
        self.game_object = GameObject("camera")
        self.to_render = game_objects
        self.width = width
        self.height = height

    def render(self, screen, offset=0.5):
        for obj in self.to_render:
            mx = self.game_object.transform.position.x
            my = self.game_object.transform.position.y
            x = self.to_render[obj].transform.position.x
            y = self.to_render[obj].transform.position.y

            offsetx = mx - x
            offsety = my - y
            self.to_render[obj].render(screen, self.width / 2 + offsetx, self.height / 2 + offsety)
