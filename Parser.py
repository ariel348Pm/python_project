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
            if child.tag in Shape.basic_shapes:
                shapes_list.append(XmlParser.get_basic(child))
            elif (child.tag in Composite.complex_shapes) or (child.tag == "Composite"):
                shapes_list.append(XmlParser.get_composite(child))
            else:
                raise Exception("Unknown shape")

        return [shape for shape in shapes_list if shape is not None]

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

    def print_tree(self):
        root = self.tree_root
        self.print_tree_wrapped(root)

    @staticmethod
    def print_tree_wrapped(root):
        print(root.tag, root.attrib)
        for child in root:
            XmlParser.print_tree_wrapped(child)

