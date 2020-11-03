import numpy as np
from Enviroment import Manager
from Parser import XmlParser
from Shapes.Point import Point
from Shapes.Basic import Line, Circle, Polygon
from copy import deepcopy

# l1 = Line(Point((100, 100)), Point((50, 100)), (130, 255, 0), 5)
# l2 = deepcopy(l1)
# l3 = deepcopy(l1)
# l4 = deepcopy(l1)
# l5 = deepcopy(l1)
# l2.transform((100, -30), 0, 1)
# l3.transform((100, -30), 60, 1)
# l4.transform((100, -100), 0, 2)
# l5.transform((100, -150), 90, 3)

# c1 = Circle(Point((100, 40)), 20, (255, 255, 255))
# c2 = deepcopy(c1)
# c3 = deepcopy(c1)
# c4 = deepcopy(c1)
# c5 = deepcopy(c1)
# c2.transform((100, -30), 0, 1)
# c3.transform((100, -50), 60, 1)
# c4.transform((100, -100), 0, 2)
# c5.transform((100, -150), 90, 3)

# r1 = Rectangle(Point((50, 50)), Point((80, 100)), (0, 255, 255))
# r2 = deepcopy(r1)
# r3 = deepcopy(r1)
# r4 = deepcopy(r1)
# r5 = deepcopy(r1)
# r2.transform((100, -30), 45, 1)
# r3.transform((100, -50), 60, 1)
# r4.transform((100, -100), 0, 2)
# r5.transform((100, -150), 90, 3)
# l2 = Line(Point((0, 0)), Point((40, 100)), (0, 30, 200), 10)
# c1 = Circle(Point((100, 100)), 30, (0, 255, 0), 5, (0, 125, 255))
# c2 = Circle(Point((100, 100)), 30, (0, 255, 0), 5, (0, 0, 255))
# c1.transform((50, -100), 135, 2)
# r1 = Rectangle(Point((300, 300)), Point((400, 350)), (255, 255, 255), 5, (60, 255, 255))
# pts = [Point((50, 10)), Point((90, 120)), Point((150, 130)), Point((100, 30))]
# p1 = Polygon(pts, (255, 45, 80), 2)
# p2 = deepcopy(p1)
# p3 = deepcopy(p1)
# p4 = deepcopy(p1)
# p5 = deepcopy(p1)
# p2.transform((100, -30), 0, 1)
# p3.transform((100, -50), 60, 1)
# p4.transform((100, -100), 0, 2)
# p5.transform((100, -150), 90, 3)

image = 255 * np.ones((512, 512, 3), np.uint8)

manager = Manager(image)
# manager.add_sprite(l1)
# manager.add_sprite(l2)
# manager.add_sprite(l3)
# manager.add_sprite(l4)
# manager.add_sprite(l5)
#
# manager.add_sprite(c1)
# manager.add_sprite(c2)
# manager.add_sprite(c3)
# manager.add_sprite(c4)
# manager.add_sprite(c5)
#
# manager.add_sprite(p1)
# manager.add_sprite(p2)
# manager.add_sprite(p3)
# manager.add_sprite(p4)
# manager.add_sprite(p5)

path = "myshape.xml"
parser = XmlParser(path)
shapes = parser.get_shapes()
for shape in shapes:
    shape.transform((150, -150), 0, 1)
    manager.add_sprite(shape)

manager.draw_all()

