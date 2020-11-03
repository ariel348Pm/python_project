import cv2 as cv
import numpy as np
from abc import abstractmethod, ABC
import re
from Shapes.Point import Point


class Sprite(ABC):

    @abstractmethod
    def draw_on(self, canvas):
        pass


class Shape(Sprite):
    def __init__(self, new_specifications):
        specifications = {"Color": (0, 0, 0), "FillingColor": None, "Thickness": 5,
                          "TranslateX": 0, "TranslateY": 0, "Rotate": 0, "Scale": 1}
        specifications.update(new_specifications)
        self.points = np.array(object)
        self.center = None
        self.specifications = Shape.parse_specifications(specifications)

    def transform(self, translation=(0, 0), rotation=0, scale_change=1):
        translation_x, translation_y = translation

        self.points = self.points - self.center.reshape((2, 1))
        self.points = self.rotate(-rotation, self.points)
        self.points = self.scale(scale_change, self.points)
        self.points = self.points + self.center.reshape((2, 1))
        self.points = Shape.translate((translation_x, -translation_y), self.points)
        self.unpack_points()

    def get_center(self):
        return self.center

    @staticmethod
    def translate(translation, points):
        return points + Point(translation).reshape((2, 1))

    @staticmethod
    def rotate(rotation, points):
        theta = np.radians(rotation)
        c, s = np.cos(theta), np.sin(theta)
        rot_mat = np.array(((c, -s), (s, c)))
        return rot_mat @ points

    @staticmethod
    def scale(scale_change, points):
        return points * scale_change

    @staticmethod
    def parse_specifications(specifications):
        specifications["Color"] = Shape.parse_color(specifications["Color"])
        specifications["FillingColor"] = Shape.parse_color(specifications["FillingColor"])
        specifications["Thickness"] = int(specifications["Thickness"])
        specifications["TranslateX"] = int(specifications["TranslateX"])
        specifications["TranslateY"] = int(specifications["TranslateY"])
        specifications["Rotate"] = int(specifications["Rotate"])
        specifications["Scale"] = int(specifications["Scale"])
        return specifications

    @staticmethod
    def parse_color(color):
        bgr_regex = r"^\((?:\d|[1-9][0-9]|1\d{2}|2[0-4]\d|25[0-5])(?:" \
                    r",\s*(?:\d|[1-9][0-9]|1\d{2}|2[0-4]\d|25[0-5])){2}\)$"

        colors = {"Black": (0, 0, 0), "White": (255, 255, 255), "Red": (0, 0, 255), "Green": (0, 255, 0),
                  "Blue": (255, 0, 0), "Cyan": (255, 255, 0), "Magenta": (255, 0, 255), "Yellow": (0, 255, 255)}

        if color is None:
            return None
        elif color in colors:
            return colors[color]
        elif re.search(bgr_regex, color):
            return tuple(map(int, color.replace('(', '').replace(')', '').split(', ')))
        else:
            raise Exception("Color unrecognized")

    @abstractmethod
    def unpack_points(self):
        pass


class Line(Shape):

    def __init__(self, p1, p2, specifications):
        super().__init__(specifications)
        self.p1 = p1
        self.p2 = p2
        self.color = specifications["Color"]
        self.thickness = specifications["Thickness"]
        self.points = np.array([p1, p2]).T
        self.center = self.points.mean(axis=1)
        self.transform((specifications["TranslateX"], specifications["TranslateY"]), specifications["Rotate"],
                       specifications["Scale"])

    def unpack_points(self):
        self.p1 = Point((self.points[0, 0], self.points[1, 0]))
        self.p2 = Point((self.points[0, 1], self.points[1, 1]))

    def draw_on(self, canvas):
        cv.line(canvas, (round(self.p1.x), round(self.p1.y)), (round(self.p2.x), round(self.p2.y)), self.color,
                self.thickness)


class Circle(Shape):

    def __init__(self, center, radius, specifications):
        super().__init__(specifications)
        self.center = center
        self.radius = radius
        self.color = specifications["Color"]
        self.thickness = specifications["Thickness"]
        self.fill = specifications["FillingColor"]
        self.points = np.array([self.center + Point((0, self.radius)), self.center - Point((0, self.radius))]).T
        self.transform((specifications["TranslateX"], specifications["TranslateY"]), specifications["Rotate"],
                       specifications["Scale"])

    def unpack_points(self):
        p1 = Point((self.points[0, 0], self.points[1, 0]))
        p2 = Point((self.points[0, 1], self.points[1, 1]))
        self.radius = p1.dist(p2) / 2
        self.center = (p1 + p2) / 2

    def draw_on(self, canvas):
        if self.fill is not None:
            cv.circle(canvas, (round(self.center.x), round(self.center.y)), round(self.radius), self.fill, -1)

        cv.circle(canvas, (round(self.center.x), round(self.center.y)), round(self.radius), self.color, self.thickness)


class Polygon(Shape):

    def __init__(self, pts, specifications):
        super().__init__(specifications)
        self.points = np.array(pts).T
        self.color = specifications["Color"]
        self.thickness = specifications["Thickness"]
        self.fill = specifications["FillingColor"]
        self.center = self.points.mean(axis=1)
        self.transform((specifications["TranslateX"], specifications["TranslateY"]), specifications["Rotate"],
                       specifications["Scale"])

    def unpack_points(self):
        pass

    def draw_on(self, canvas):
        self.points = self.points.T
        self.points = self.points.reshape((-1, 1, 2))

        if self.fill is not None:
            cv.fillPoly(canvas, np.int32([self.points]), self.fill)

        cv.polylines(canvas, np.int32([self.points]), True, self.color, self.thickness)
