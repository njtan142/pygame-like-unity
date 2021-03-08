import math
import random


class Collision:

    def __init__(self, points, pygame):
        self.points = points
        self.edges = self.get_edges()
        self.sides = None
        self.pygame = pygame
        self.origin = None
        self.calculate_origin()

    def draw_lines(self, screen):
        for edge in self.edges:
            start = edge[0][0] + screen.get_width() / 2, -edge[0][1] + screen.get_height() / 2
            end = edge[1][0] + screen.get_width() / 2, -edge[1][1] + screen.get_height() / 2
            self.pygame.draw.line(screen, (0, 255, 0), start, end, 2)
        origin = self.pygame.rect.Rect(self.origin[0] + screen.get_width() / 2,
                                       -self.origin[1] + screen.get_height() / 2,
                                       1, 1)
        self.pygame.draw.rect(screen, (0, 255, 0), origin)

    def calculate_origin(self):
        mean_x = 0
        mean_y = 0
        for x, y in self.points:
            mean_x += x
            mean_y += y
        mean_x = mean_x / len(self.points)
        mean_y = mean_y / len(self.points)
        self.origin = (mean_x, mean_y)

    def get_edges(self):
        edges = []
        for start_point in self.points:
            for end_point in self.points:
                if start_point != end_point:
                    if start_point[1] - end_point[1] >= 0:
                        if [end_point, start_point] not in edges:
                            edges.append([start_point, end_point])
        return edges

    def move(self, horizontal, vertical):
        for i in range(len(self.points)):
            self.points[i] = self.points[i][0] + horizontal, self.points[i][1] + vertical
        self.edges = self.get_edges()
        self.calculate_origin()
