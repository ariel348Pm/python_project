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
        for shape in self.shapes:
            shape.transform(translation, rotation, scale_change)

    def unpack_points(self):
        for shape, point in zip(self.shapes, self.points):
            shape.set_center(point)

    def draw_on(self, canvas):
        for shape in self.shapes:
            shape.draw_on(canvas)
