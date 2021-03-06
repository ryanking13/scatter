import random
from PIL import ImageDraw
import color_palette
from functions import *
import logger
from lane import ParticleLane
import particle


def snow_lane(img, n_lanes, n_frames, min_speed, max_speed,
              particle_size_range, palette):

    lanes = []
    weighted_size_list = generate_weighted_list(particle_size_range[0], particle_size_range[1])
    for i in range(n_lanes):
        position = (random.randint(0, img.size[0]), random.randint(0, img.size[1]))
        speed_x = random.randint(min_speed[0], max_speed[0])
        speed_y = random.randint(min_speed[1], max_speed[1])
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
        color = random.choice(palette)

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
            # mask = p.advanced_draw(mask)
            p.move()

            frame = Image.composite(frame, mask, mask=mask)  # add particle to frame

        frames.append(frame)

        logger.log('[*] Working on ({}/{}) frame...'.format(i+1, n_frames))

    return frames


def decorate(img, args):

    non_continuous_decoraters = {

    }

    continuous_decoraters = {
        'SNOW': snow_lane,
    }

    particle_type = args['type']
    continuous = args['continuous']
    density = args['density']
    n_frames = args['n_frames']
    speed = args['speed']
    min_speed = (speed[0], speed[2])
    max_speed = (speed[1], speed[3])
    size = args['size']
    palette = color_palette.get_palette(args['palette'])

    if continuous:
        try:
            decorator = continuous_decoraters[particle_type]
            return decorator(img, n_lanes=density, n_frames=n_frames,
                             min_speed=min_speed, max_speed=max_speed,
                             particle_size_range=size, palette=palette)
        except KeyError:
            raise
    else:
        try:
            decorator = non_continuous_decoraters[particle_type]
        except KeyError:
            raise