import xml.etree.ElementTree as Et
from Shapes.Point import Point
from Shapes.Basic import Line, Circle, Polygon
from enum import Enum


class XmlParser(object):

    composite_list = list()

    def __init__(self, path):
        self.tree = Et.parse(path)
        self.tree_root = self.tree.getroot()
        # self.basic_shapes = Enum("basic_shapes", ["Line", "Circle", "Triangle", "Rectangle", "polygon"])
        self.basic_shapes = ["Line", "Circle", "Triangle", "Rectangle", "polygon"]  # todo: enum

    def get_shapes(self):
        shapes_list = list()
        for child in self.tree_root:
            if child.tag in self.basic_shapes:
                shapes_list.append(self.get_basic(child))
            else:
                shapes_list.append(self.get_composite(child))

        return shapes_list

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

