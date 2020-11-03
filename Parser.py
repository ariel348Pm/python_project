import xml.etree.ElementTree as Et
from Shapes.Point import Point
from Shapes.Basic import Line, Circle, Polygon


class XmlParser(object):

    composite_list = list()

    def __init__(self, path):
        self.tree = Et.parse(path)
        self.tree_root = self.tree.getroot()
        self.basic_list = ["Line", "Circle", "Triangle", "Rectangle", "polygon"]  # todo: enum

    def get_shapes(self):
        shapes_list = list()
        for child in self.tree_root:
            if child.tag in self.basic_list:
                shapes_list.append(self.get_basic(child))
            else:
                shapes_list.append(self.get_composite(child))

        return shapes_list

    def get_basic(self, root):
        color = (0, 0, 0)
        fill = None
        thickness = 5

        translate_x = 0
        translate_y = 0

        rotate = 0
        scale = 1

        if "Color" in root.attrib:
            color = XmlParser.parse_color(root.attrib["Color"])  # todo: no if
        if "FillingColor" in root.attrib:
            fill = XmlParser.parse_color(root.attrib["FillingColor"])
        if "Thickness" in root.attrib:
            thickness = int(root.attrib["Thickness"])

        if "TranslateX" in root.attrib:
            translate_x = int(root.attrib["TranslateX"])
        if "TranslateY" in root.attrib:
            translate_y = int(root.attrib["TranslateY"])
        if "Rotate" in root.attrib:
            rotate = int(root.attrib["Rotate"])
        if "Scale" in root.attrib:
            scale = int(root.attrib["Scale"])

        if root.tag == "Line":
            p1 = Point((int(root[0].attrib["X"]), int(root[0].attrib["Y"])))
            p2 = Point((int(root[1].attrib["X"]), int(root[1].attrib["Y"])))

            return Line(p1, p2, color, thickness)

        if root.tag == "Circle":
            center = Point((int(root.attrib["X"]), int(root.attrib["Y"])))
            radius = int(root.attrib["Radius"])

            return Circle(center, radius, color, thickness, fill)

        if root.tag in ["Triangle", "Rectangle", "Polygon"]:
            points = list()
            for child in root:
                points.append(Point((int(child.attrib["X"]), int(child.attrib["Y"]))))

            return Polygon(points, color, thickness, fill)

    def get_composite(self, root):
        pass

    def print_tree(self):
        root = self.tree_root
        self.print_tree_wrapped(root)

    @staticmethod
    def print_tree_wrapped(root):
        print(root.tag, root.attrib)
        for child in root:
            XmlParser.print_tree_wrapped(child)

    @staticmethod
    def parse_color(color):
        colors = {"Black": (0, 0, 0), "White": (255, 255, 255), "Red": (0, 0, 255), "Green": (0, 255, 0),
                  "Blue": (255, 0, 0), "Cyan": (255, 255, 0), "Magenta": (255, 0, 255), "Yellow": (0, 255, 255)}

        if color in colors:
            return colors[color]
        else:
            return tuple(map(int, color.replace('(', '').replace(')', '').split(', ')))  # todo: make regex
