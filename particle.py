import random


class Particle:

    def __init__(self, max_x, max_y, size, speed_x, speed_y):
        self._max_x = max_x
        self._max_y = max_y
        self._size = size

        self._x = random.randint(0, max_x)
        self._y = random.randint(-max_y, 0)

        self._speed_x = speed_x
        self._speed_y = speed_y

    def move(self):

        self._x += self._speed_x
        self._y += self._speed_y

    def get_position(self):

        return self._x, self._y

    def get_size(self):
        return self._size


class Snow(Particle):

    def __init__(self, max_x, max_y, size, speed_x, speed_y):
        super().__init__(max_x, max_y, size, speed_x, speed_y)
        self.color = 0