import xml.etree.ElementTree as Et
from Shapes.Point import Point
from Shapes.Basic import Shape, Circle, Polygon
from Shapes.Complex import Composite
from copy import deepcopy


class XmlParser(object):

    def __init__(self, path):
        self.tree = Et.parse(path)
        self.tree_root = self.tree.getroot()

    def get_shapes(self, root=None):
        if root is None:
            root = self.tree_root
        shapes_list = list()
        for child in root:
            shapes_list.append(XmlParser.get_shape(child))

        return [shape for shape in shapes_list if shape is not None]

    @staticmethod
    def get_shape(root):
        if root.tag in Shape.basic_shapes:
            return XmlParser.get_basic(root)

        return XmlParser.get_composite(root)

    @staticmethod
    def get_basic(root):
        specifications = root.attrib

        if root.tag == "Circle":
            center = Point((int(root.attrib["X"]), int(root.attrib["Y"])))
            radius = int(root.attrib["Radius"])
            return Circle(center, radius, specifications)

        if root.tag in ["Line", "Triangle", "Rectangle", "Polygon"]:
            points = list()
            for child in root:
                points.append(Point((int(child.attrib["X"]), int(child.attrib["Y"]))))

            return Polygon(points, specifications)

    @staticmethod
    def get_composite(root):
        if (root.tag not in Composite.complex_shapes) and (root.tag != "Composite"):
            raise Exception("Unknown shape")

        specifications = root.attrib
        if root.tag == "Composite":
            name = specifications["Name"]
            draw = specifications["Draw"]
            if name in [child.tag for child in root]:
                shapes = XmlParser.get_fractal_shapes(root, 5, name)
            else:
                shapes = XmlParser.get_shapes(root)
            Composite.complex_shapes[name] = Composite(name, shapes, root.attrib)
            if draw == "No":
                return None
        else:
            name = root.tag

        composite = deepcopy(Composite.complex_shapes[name])
        composite.copy_transform_data(specifications)
        composite.transform(composite.get_center(),
                            (composite.specifications["TranslateX"], composite.specifications["TranslateY"]),
                            composite.specifications["Rotate"], composite.specifications["Scale"])
        return composite

    @staticmethod
    def get_fractal_shapes(root, depth, name):
        shapes = list()
        if depth <= 0:
            return None

        for child in root:
            if child.tag == name:
                composite_shapes = XmlParser.get_fractal_shapes(root, depth - 1, name)
                if composite_shapes is None:
                    continue
                shape = Composite(name, composite_shapes, child.attrib)
            else:
                shape = XmlParser.get_shape(child)

            shapes.append(shape)

        return shapes

    def print_tree(self):
        root = self.tree_root
        self.print_tree_wrapped(root)

    @staticmethod
    def print_tree_wrapped(root):
        print(root.tag, root.attrib)
        for child in root:
            XmlParser.print_tree_wrapped(child)
