import numpy as np
from Shapes.Basic import Shape


class Composite(Shape):
    complex_shapes = {}

    def __init__(self, name, shapes, specifications={}):
        super().__init__(specifications)
        self.name = name
        self.shapes = shapes
        centers = np.array([shape.get_center() for shape in shapes]).T
        self.center = centers.mean(axis=1)
        self.transform(self.center, (self.specifications["TranslateX"], self.specifications["TranslateY"]),
                       self.specifications["Rotate"], self.specifications["Scale"])

    def transform(self, center, translation=(0, 0), rotation=0, scale_change=1):
        for shape in self.shapes:
            shape.transform(center, translation, rotation, scale_change)

    def apply_transform(self, new_specifications):
        specifications = {"TranslateX": 0, "TranslateY": 0, "Rotate": 0, "Scale": 1}
        specifications.update(Shape.parse_specifications(new_specifications))
        self.transform(self.center, (specifications["TranslateX"], specifications["TranslateY"]),
                       specifications["Rotate"], specifications["Scale"])

    def unpack_points(self):
        pass

    def draw_on(self, canvas):
        for shape in self.shapes:
            shape.draw_on(canvas)
