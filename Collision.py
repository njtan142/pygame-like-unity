import math
import random

def distance(point1, point2):
    x = (point2[0] - point1[0]) ** 2
    y = (point2[1] - point1[1]) ** 2
    return (x + y) ** 0.5



class Collision:

    def __init__(self, points, pygame):
        self.points = points
        self.edges = self.get_edges()
        self.sides = self.calculate_sides()
        self.pygame = pygame
        self.origin = self.calculate_origin()
        print(self.sides)
       

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
        return (mean_x, mean_y)

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
        self.origin = self.calculate_origin()
        self.sides = self.calculate_sides()

    def calculate_sides(self):
        sides = []
        for edge in self.edges:
            x = edge[0][0] + edge[1][0]
            y = edge[0][1] + edge[1][1]
            sides.append((x/2,y/2))
        return sides

    def point_collision(self, point):
        index = 0
        nearest_point = None
        nearest_distance = None
        for side in self.sides:
            d = distance(point, side)
            if nearest_distance is None:
                nearest_distance = d
                nearest_point = side
            elif nearest_distance > d:
                nearest_distance = d
                nearest_point = side
        return nearest_point, nearest_distance, point

    def multiple_collision(self, points):
        for point in points:
            print(self.point_collision(point))
