import cv2 as cv
import numpy as np
from Shapes.Point import Point


class Sprite(object):
    def draw_on(self, canvas):
        pass


class Shape(Sprite):
    def __init__(self):
        self.points = np.array()
        self.center = None

    def transform(self, translation=(0, 0), rotation=0, scale_change=1):
        translation_x, translation_y = translation

        self.points = self.points - self.center.reshape((2, 1))
        self.rotate(-rotation)
        self.scale(scale_change)
        self.points = self.points + self.center.reshape((2, 1))
        self.translate((translation_x, -translation_y))
        self.unpack_points()

    def translate(self, translation):
        self.points = self.points + Point(translation).reshape((2, 1))
        return

    def rotate(self, rotation):
        theta = np.radians(rotation)
        c, s = np.cos(theta), np.sin(theta)
        rot_mat = np.array(((c, -s), (s, c)))

        pts = np.array([list(self.points[0, :]), list(self.points[1, :])])
        self.points = rot_mat @ pts
        return

    def scale(self, scale_change):
        self.points = self.points * scale_change
        return

    def unpack_points(self):
        pass


class Line(Shape):

    def __init__(self, p1, p2, color=(255, 255, 255), thickness=5):
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.thickness = thickness
        self.points = np.array([p1, p2]).T
        self.center = self.points.mean(axis=1)

    def unpack_points(self):
        self.p1 = Point((self.points[0, 0], self.points[1, 0]))
        self.p2 = Point((self.points[0, 1], self.points[1, 1]))

    def draw_on(self, canvas):
        cv.line(canvas, (round(self.p1.x), round(self.p1.y)), (round(self.p2.x), round(self.p2.y)), self.color,
                self.thickness)


class Circle(Shape):

    def __init__(self, center, radius, color=(255, 255, 255), thickness=5, fill=None):
        self.center = center
        self.radius = radius
        self.color = color
        self.thickness = thickness
        self.fill = fill
        self.points = np.array([self.center + Point((0, self.radius)), self.center - Point((0, self.radius))]).T
        return

    def unpack_points(self):
        p1 = Point((self.points[0, 0], self.points[1, 0]))
        p2 = Point((self.points[0, 1], self.points[1, 1]))
        self.radius = p1.dist(p2) / 2
        self.center = (p1 + p2) / 2
        return

    def draw_on(self, canvas):
        if self.fill is not None:
            cv.circle(canvas, (round(self.center.x), round(self.center.y)), round(self.radius), self.fill, -1)

        cv.circle(canvas, (round(self.center.x), round(self.center.y)), round(self.radius), self.color, self.thickness)


# class Rectangle(Shape):
#
#     def __init__(self, top_left, bottom_right, color=(255, 255, 255), thickness=5, fill=None):
#         self.top_left = top_left
#         self.bottom_right = bottom_right
#         self.color = color
#         self.thickness = thickness
#         self.fill = fill
#         self.points = np.array([top_left, bottom_right]).T
#         self.center = self.points.mean(axis=1).reshape((2, 1))
#         return
#
#     def unpack_points(self):
#         self.top_left = Point((self.points[0, 0], self.points[1, 0]))
#         self.bottom_right = Point((self.points[0, 1], self.points[1, 1]))
#
#     def draw_on(self, canvas):
#         if self.fill is not None:
#             cv.rectangle(canvas, (round(self.top_left.x), round(self.top_left.y)),
#                          (round(self.bottom_right.x), round(self.bottom_right.y)), self.fill, -1)
#
#         cv.rectangle(canvas, (round(self.top_left.x), round(self.top_left.y)),
#                      (round(self.bottom_right.x), round(self.bottom_right.y)), self.color, self.thickness)


class Polygon(Shape):

    def __init__(self, pts, color=(255, 255, 255), thickness=5, fill=None):
        self.points = self.points_to_list(pts)
        self.color = color
        self.thickness = thickness
        self.fill = fill
        self.center = self.points.mean(axis=1)
        return

    @staticmethod
    def points_to_list(pts):
        l = list()
        for point in pts:
            l.append([point.x, point.y])

        vertices = np.array(l).T
        return vertices

    def unpack_points(self):
        pass

    def draw_on(self, canvas):
        self.points = self.points.T
        self.points = self.points.reshape((-1, 1, 2))

        if self.fill is not None:
            cv.fillPoly(canvas, [self.points], self.fill)

        cv.polylines(canvas, np.int32([self.points]), True, self.color, self.thickness)
