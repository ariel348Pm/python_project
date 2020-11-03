from Shapes.Basic import Shape


class Composite(Shape):

    def __init__(self, name, shapes):
        self.name = name
        self.shapes = shapes

    def draw_on(self, canvas):
        for shape in self.shapes:
            shape.draw_on(canvas)
