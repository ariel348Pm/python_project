import xml.etree.ElementTree as Et
from Shapes.Point import Point
from Shapes.Basic import Shape, Line, Circle, Polygon
from Shapes.Complex import Composite
from copy import deepcopy


class XmlParser(object):

    def __init__(self, path):
        self.tree = Et.parse(path)
        self.tree_root = self.tree.getroot()

    @staticmethod
    def get_shapes(root):
        shapes_list = list()
        for child in root:
            shapes_list.append(XmlParser.get_shape(child))

        return [shape for shape in shapes_list if shape is not None]

    @staticmethod
    def get_shape(root):
        if root.tag in Shape.basic_shapes:
            return XmlParser.get_basic(root)
        elif (root.tag in Composite.complex_shapes) or (root.tag == "Composite"):
            return XmlParser.get_composite(root)
        else:
            raise Exception("Unknown shape")

    @staticmethod
    def get_basic(root):
        specifications = root.attrib

        if root.tag == "Line":
            p1 = Point((int(root[0].attrib["X"]), int(root[0].attrib["Y"])))
            p2 = Point((int(root[1].attrib["X"]), int(root[1].attrib["Y"])))
            return Line(p1, p2, specifications)

        if root.tag == "Circle":
            center = Point((int(root.attrib["X"]), int(root.attrib["Y"])))
            radius = int(root.attrib["Radius"])
            return Circle(center, radius, specifications)

        if root.tag in ["Triangle", "Rectangle", "Polygon"]:
            points = list()
            for child in root:
                points.append(Point((int(child.attrib["X"]), int(child.attrib["Y"]))))

            return Polygon(points, specifications)

    @staticmethod
    def get_composite(root):
        specifications = root.attrib
        name = root.tag
        if name == "Composite":
            name = specifications["Name"]
            draw = specifications["Draw"]
            if name in [child.tag for child in root]:
                shapes = XmlParser.get_fractal_shapes(root, 5, name, root)
            else:
                shapes = XmlParser.get_shapes(root)
            Composite.complex_shapes[name] = Composite(name, shapes, root.attrib)
            if draw == "No":
                return None

        composite = deepcopy(Composite.complex_shapes[name])
        composite.copy_transform_data(Shape.parse_specifications(specifications))
        composite.transform(composite.get_center(),
                            (composite.specifications["TranslateX"], composite.specifications["TranslateY"]),
                            composite.specifications["Rotate"], composite.specifications["Scale"])
        return composite

    @staticmethod
    def get_fractal_shapes(root, depth, name, composite_root):
        shapes = list()
        new_shapes = list()
        if depth <= 0:
            return None

        for child in root:
            if child.tag == name:
                shape = XmlParser.get_fractal_shapes(composite_root, depth - 1, name, composite_root)
                if shape is not None:
                    shapes.extend(shape)
            else:
                shapes.append(XmlParser.get_shape(child))

        return shapes

    def print_tree(self):
        root = self.tree_root
        self.print_tree_wrapped(root)

    @staticmethod
    def print_tree_wrapped(root):
        print(root.tag, root.attrib)
        for child in root:
            XmlParser.print_tree_wrapped(child)
