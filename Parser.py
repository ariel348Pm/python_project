import xml.etree.ElementTree as Et
from Shapes.Point import Point
from Shapes.Basic import Shape, Circle, Polygon
from Shapes.Complex import Composite
from copy import deepcopy


class XmlParser(object):

    def __init__(self, path):
        self.tree = Et.parse(path)
        self.tree_root = self.tree.getroot()

    def parse(self):
        return self.get_shapes(self.tree_root)

    def get_shapes(self, root):
        shapes_list = list()
        for child in root:
            shapes_list.append(self.get_shape(child))

        return [shape for shape in shapes_list if shape is not None]

    def get_shape(self, root):
        if root.tag in Shape.basic_shapes:
            return self.get_basic(root)
        if root.tag in Composite.complex_shapes:
            return self.get_composite(root)
        if root.tag == "Composite":
            return self.create_composite(root)

        raise Exception("Unknown shape")

    def get_basic(self, root):
        specifications = root.attrib

        if root.tag == "Circle":
            center = Point((int(root.attrib["X"]), int(root.attrib["Y"])))
            radius = int(root.attrib["Radius"])
            return Circle(center, radius, specifications)

        elif root.tag in Shape.basic_shapes:
            points = list()
            for child in root:
                points.append(Point((int(child.attrib["X"]), int(child.attrib["Y"]))))

            return Polygon(points, specifications)

    def get_composite(self, root):
        specifications = root.attrib
        name = root.tag

        composite = deepcopy(Composite.complex_shapes[name])
        composite.apply_transform(specifications)

        return composite

    def create_composite(self, root):
        specifications = root.attrib
        name = specifications["Name"]
        if name in [child.tag for child in root]:
            shapes = self.get_fractal_shapes(root, 5, name)
        else:
            shapes = self.get_shapes(root)

        if name in Composite.complex_shapes:
            Warning("Composite already defined!")
        Composite.complex_shapes[name] = Composite(name, shapes, root.attrib)

        return None

    def get_fractal_shapes(self, root, depth, name):
        shapes = list()
        if depth <= 0:
            return None

        for child in root:
            if child.tag == name:
                composite_shapes = self.get_fractal_shapes(root, depth - 1, name)
                if composite_shapes is None:
                    continue
                shape = Composite(name, composite_shapes, child.attrib)
            else:
                shape = self.get_shape(child)

            shapes.append(shape)

        return shapes

