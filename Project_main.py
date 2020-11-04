import numpy as np
from Enviroment import Manager
from Parser import XmlParser

image = 255 * np.ones((600, 800, 3), np.uint8)
manager = Manager(image)

path = "my_shapes.xml"
parser = XmlParser(path)
shapes = XmlParser.get_shapes(parser.tree_root)
manager.add_sprites(shapes)
manager.draw_all()
save_path = "result.jpg"
manager.save_canvas(save_path)
