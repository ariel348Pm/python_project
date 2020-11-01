import numpy as np


class Point(np.ndarray):
    """
    n-dimensional point used for locations.
    inherits +, -, * (as dot-product)
    > p1 = Point([1, 2])
    > p2 = Point([4, 5])
    > p1 + p2
    Point([5, 7])
    """

    def __new__(cls, input_array=(0, 0)):
        """
        :param cls:
        :param input_array: Defaults to 2d origin
        """
        obj = np.asarray(input_array).view(cls)
        return obj

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def __eq__(self, other):
        return np.array_equal(self, other)

    def __ne__(self, other):
        return not np.array_equal(self, other)

    def __iter__(self):
        for x in np.nditer(self):
            yield x.item()

    def dist(self, other):
        """
        :return: Euclidean distance
        """
        return np.linalg.norm(self - other)
