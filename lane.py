import random


# defines the lane of particles ( for continuous movement of particle )
class ParticleLane:

    def __init__(self, image_size, base_position, n_frames, particle_size, speed_x, speed_y):

        self._max_x = image_size[0]
        self._max_y = image_size[1]

        self._start_x = base_position[0]
        self._start_y = base_position[1]
        self._n_frames = n_frames
        self._r = particle_size
        self._speed_x = speed_x
        self._speed_y = speed_y

        self._position = self._set_initial_position()

    # set initial position of particle
    # other particles will be generated according to initial position
    def _set_initial_position(self):

        top_y = 0
        if self._speed_y < 0:
            top_y = self._max_y

        top_x = self._start_x + self._speed_x * ((self._start_y - top_y) / self._speed_y)  # d = vt
        frame_offset = random.randint(0, self._n_frames - 1)

        init_x = int(top_x - self._speed_x * frame_offset)
        init_y = int(top_y - self._speed_y * frame_offset)

        return init_x, init_y

    # check particle's position is inside image
    def _is_inside_image(self):

        going_right = self._speed_x > 0
        going_down = self._speed_y > 0

        lx = self._position[0] - self._r
        rx = self._position[0] + self._r
        uy = self._position[1] - self._r
        dy = self._position[1] + self._r

        chk = True

        if going_right:
            chk = chk and (lx < self._max_x)
        else:
            chk = chk and (rx > 0)

        if going_down:
            chk = chk and (uy < self._max_y)
        else:
            chk = chk and (dy > 0)

        return chk

    # get all particles' position in lane
    def get_positions(self):

        positions = []

        while self._is_inside_image():
            positions.append(self._position)

            next_x = self._position[0] + self._speed_x * self._n_frames
            next_y = self._position[1] + self._speed_y * self._n_frames
            self._position = (next_x, next_y)

        return positions

    # get lane's size, speed
    def get_lane_info(self):
        return self._r, self._speed_x, self._speed_y
