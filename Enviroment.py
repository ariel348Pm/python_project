import cv2 as cv


class Manager(object):

    def __init__(self, canvas):
        self.sprites = list()
        self.canvas = canvas

    def add_sprite(self, sprite):
        self.sprites.append(sprite)

    def remove_sprite(self, sprite):
        self.sprites.remove(sprite)

    def draw_all(self):
        for sprite in self.sprites:
            sprite.draw_on(self.canvas)

        cv.imshow("image", self.canvas)
        cv.waitKey(0)
        cv.destroyAllWindows()
