from PygameUnity.game_object import GameObject


class Camera:

    def __init__(self, width, height, game_objects):
        self.game_object = GameObject("camera")
        self.objects = game_objects
        self.width = width
        self.height = height
        self.z_positions = []
        self.layers = []
        self.sort()

    def render(self, screen):
        for position in self.z_positions:
            for layer in self.layers:
                for obj in self.objects:
                    if self.objects[obj].transform.position.z != position:
                        continue
                    if self.objects[obj].renderer.layer != layer:
                        continue
                    mx = self.game_object.transform.position.x
                    my = self.game_object.transform.position.y
                    x = self.objects[obj].transform.position.x
                    y = self.objects[obj].transform.position.y

                    offset_x = x - mx
                    offset_y = my - y
                    self.objects[obj].render(screen, self.width / 2 + offset_x, self.height / 2 + offset_y)

    def sort(self):
        for obj in self.objects:
            if self.objects[obj].transform.position.z not in self.z_positions:
                self.z_positions.append(self.objects[obj].transform.position.z)
            if self.objects[obj].renderer.layer not in self.layers:
                self.layers.append(self.objects[obj].renderer.layer)

        self.z_positions.sort()
        self.layers.sort()
        print(self.layers)
