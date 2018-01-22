import random
from PIL import ImageDraw
import color_palette
from functions import *
from lane import ParticleLane
import particle


def snow_lane(img, n_lanes=200, n_frames=50, min_speed=(-2, 2), speed_deviation=(4, 3),
              min_particle_size=1, particle_size_deviation=10):

    lanes = []
    weighted_size_list = generate_weighted_list(min_particle_size, min_particle_size + particle_size_deviation)
    for i in range(n_lanes):
        position = (random.randint(0, img.size[0]), random.randint(0, img.size[1]))
        speed_x = min_speed[0] + random.randint(0, speed_deviation[0])
        speed_y = min_speed[1] + random.randint(0, speed_deviation[1])
        # size = min_particle_size + random.randint(0, particle_size_deviation)
        size = random.choice(weighted_size_list)

        lane = ParticleLane(
            image_size=img.size,
            base_position=position,
            n_frames=n_frames,
            particle_size=size,
            speed_x=speed_x,
            speed_y=speed_y,
        )

        lanes.append(lane)

    snow_particles = []
    for lane in lanes:
        positions = lane.get_positions()
        particle_size, speed_x, speed_y = lane.get_lane_info()
        color = random.choice(color_palette.BRIGHT)

        for pos in positions:
            snow = particle.Snow(
                xy=img.size,
                size=particle_size,
                speed_x=speed_x,
                speed_y=speed_y,
                position=pos,
                color=color
            )

            snow_particles.append(snow)

    frames = []  # frames that will compose animated image
    for i in range(n_frames):

        frame = img.copy()

        for p in snow_particles:
            mask = Image.new('RGBA', img.size, color=(255, 255, 255))  # image for masking
            board = ImageDraw.Draw(mask)

            p.draw(board)
            p.move()

            frame = Image.composite(frame, mask, mask=mask)  # add particle to frame

        frames.append(frame)

    return frames

