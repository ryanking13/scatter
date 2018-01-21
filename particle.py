import random


class Particle:

    def __init__(self, xy, size, speed_x, speed_y, position=None):
        self._max_x = xy[0]
        self._max_y = xy[1]
        self._size = size

        if not position:
            self._x = random.randint(0, self._max_x)
            self._y = random.randint(-self._max_y, 0)
        else:
            self._x = position[0]
            self._y = position[1]

        if speed_y < 0:
            self._y = random.randint(self._max_y, self._max_y * 2)

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

    def __init__(self, xy, size, speed_x, speed_y, position=None, color=(255, 255, 255)):
        super().__init__(xy, size, speed_x, speed_y, position)
        self.color = color

    def draw(self, d):

        x, y = self.get_position()
        r = self.get_size()
        col = self.color

        st_x = x - r
        st_y = y - r
        ed_x = x + r
        ed_y = y + r

        gap = r // 4  # slice will move from outline(r) to gap
        n_slices = min(50, r - gap)  # how many slices will compose one particle
        coord_offset = (r - gap) / n_slices  # how much coordinate will be changed per slice
        max_fill = 128
        fill_offset = max_fill / n_slices  # how much fill will be changed per slice
        for i in range(n_slices):
            co = int(i * coord_offset)
            fo = 255 - int(i * fill_offset)
            d.ellipse([st_x + co, st_y + co, ed_x - co, ed_y - co], fill=col + (fo,))
