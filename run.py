import argparse
from PIL import Image
import config
from functions import *
import decorator


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


def main():

    args = parse_arguments()
    img = Image.open(args.get('filename'))
    img = img.convert('P', palette=Image.ADAPTIVE, dither=Image.NONE)
    img_size = get_image_size(img)
    MAX_FRAME_SIZE = 256 * 10**3  # 256 kb

    if img_size > MAX_FRAME_SIZE:
        img = resize_image(img, img_size, MAX_FRAME_SIZE)

    frames = decorator.snow_lane(img)

    # not sure why frames[0].save() not works properly...
    initial_frame = frames[0]
    initial_frame.save('out.gif', save_all=True, append_images=frames, optimize=True, duration=30, loop=100)  # min duration : 20

if __name__ == '__main__':
    main()