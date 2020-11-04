import numpy as np
from Shapes.Basic import Shape


class Composite(Shape):
    complex_shapes = {}

    def __init__(self, name, shapes, specifications={}):
        super().__init__(specifications)
        self.name = name
        self.shapes = shapes
        self.points = np.array([shape.get_center() for shape in shapes]).T
        self.center = self.points.mean(axis=1)
        self.transform((self.specifications["TranslateX"], self.specifications["TranslateX"]),
                       self.specifications["Rotate"], self.specifications["Scale"])

    def transform(self, translation=(0, 0), rotation=0, scale_change=1):
        translation_x, translation_y = translation

        for shape in self.shapes:
            shape.points = shape.points - self.center.reshape((2, 1))
            shape.points = shape.rotate(-rotation, shape.points)
            shape.points = shape.scale(scale_change, shape.points)
            shape.points = shape.points + self.center.reshape((2, 1))
            shape.points = Shape.translate((translation_x, -translation_y), shape.points)
            shape.unpack_points()

    def unpack_points(self):
        pass

    def draw_on(self, canvas):
        for shape in self.shapes:
            shape.draw_on(canvas)
