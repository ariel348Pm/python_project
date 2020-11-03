import numpy as np
from Enviroment import Manager
from Parser import XmlParser

image = 255 * np.ones((512, 512, 3), np.uint8)
manager = Manager(image)

path = "shapes.xml"
parser = XmlParser(path)
shapes = XmlParser.get_shapes(parser.tree_root)
for shape in shapes:
    manager.add_sprite(shape)

manager.draw_all()

