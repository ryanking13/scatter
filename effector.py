from PIL import Image, ImageDraw
import sys
import math
from io import BytesIO
from particle import *
from lane import ParticleLane
import color_palette
import argparse
import config


def parse_arguments():
    """ parse command line arguments """

    parser = argparse.ArgumentParser()

    parser.add_argument('filename', help='image file that will be decorated')

    parser.add_argument('-c', '--compress', default=config.DEFAULT_COMPRESS_LEVEL,
                        help=('set compress level of output image. '
                              '(0 to 5, 0: highest compress, 5: no compress) '
                              '(default={})'.format(config.DEFAULT_COMPRESS_LEVEL)))

    parser.add_argument('-d', '--density', default=config.DEFAULT_DENSITY_LEVEL,
                        help=('set particles density. '
                              '(0 to 5, 0: most sparse, 5: most dense) '
                              '(default={})'.format(config.DEFAULT_DENSITY_LEVEL)))

    parser.add_argument('-f', '--frames', default=config.DEFAULT_N_FRAMES,
                        help=('set output image\'s number of frames '
                              '(default={})'.format(config.DEFAULT_N_FRAMES)))

    parser.add_argument('-p', '--particle', default=config.DEFAULT_PARTICLE_TYPE,
                        help=('set type of particle '
                              '(types: SNOW) '
                              '(default={}'.format(config.DEFAULT_PARTICLE_TYPE)))

    parser.add_argument('-s', '--speed', default=config.DEFAULT_SPEED_LEVEL,
                        help=('set particles speed. '
                              '(0 to 5, 0: slowest, 5: fastest) '
                              '(default={})'.format(config.DEFAULT_SPEED_LEVEL)))
    parser.add_argument('-S', '--size', default=config.DEFAULT_SIZE_LEVEL,
                        help=('set size of particle '
                              '(0 to 5, 0: smallest, 5: largest) '
                              '(default={})'.format(config.DEFAULT_SIZE_LEVEL)))

    parser.add_argument('-v', '--verbose', default=False,
                        help='print intermediate logs')

    parser.add_argument('-w', '--webp', default=False, const=True, action='store_const',
                        help='change output image format from gif to webp')

    parser.add_argument('--not_continuous', default=False, const=True, action='store_const',
                        help='output image becomes not continous')

    args = parser.parse_args()

    settings = {
        'filename': args.filename,
        'frame_size': config.FRAME_SIZES[args.compress],
        'continous': not args.not_continuous,
        'density': config.PARTICLE_NUMBERS[args.density] if args.not_continuous else config.LANE_NUMBERS[args.density],
        'n_frame': args.frames,
        'type': args.particle.upper(),
        'speed': config.SPEED_LEVELS[args.speed],
        'size': config.SIZE_LEVELS[args.size],
        'verbose': args.verbose,
        'webp': args.webp,
    }

    return settings


def generate_weighted_list(st, ed, ratio=(20, 2, 1)):

    nums = [i for i in range(st, ed+1)]

    n_boundary = len(ratio)
    boundary_offset = (ed - st + n_boundary - 1) // n_boundary

    choices = []
    for i, n in enumerate(nums):
        r = ratio[i // boundary_offset]
        choices.extend([n] * r)

    return choices


def get_image_size(image):
    tp_file = BytesIO()
    image.save(tp_file, 'GIF')

    return tp_file.tell()


def resize_image(img, cur_size, target_size):

    if cur_size <= target_size:
        return img

    shrink_ratio = target_size / cur_size
    side_ratio = math.sqrt(shrink_ratio)

    x, y = img.size
    x_ = int(x * side_ratio)
    y_ = int(y * side_ratio)
    return img.resize((x_, y_), Image.ANTIALIAS)


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
            snow = Snow(
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


def main():

    args = parse_arguments()
    img = Image.open(args.get('filename'))
    img = img.convert('P', palette=Image.ADAPTIVE, dither=Image.NONE)
    img_size = get_image_size(img)
    MAX_FRAME_SIZE = 256 * 10**3  # 256 kb

    if img_size > MAX_FRAME_SIZE:
        img = resize_image(img, img_size, MAX_FRAME_SIZE)

    frames = snow_lane(img)

    # not sure why frames[0].save() not works properly...
    initial_frame = frames[0]
    initial_frame.save('out.gif', save_all=True, append_images=frames, optimize=True, duration=30, loop=100)  # min duration : 20

if __name__ == '__main__':
    main()