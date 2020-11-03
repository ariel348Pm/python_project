import numpy as np


class Point(np.ndarray):

    def __new__(cls, input_array=(0, 0)):
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

    def dist(self, other):
        return np.linalg.norm(self - other)
