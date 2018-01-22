import argparse
from PIL import Image
import config
from functions import *
import decorators

verbose = False  # value will be set on parse_arguments() function


def parse_arguments():
    """ parse command line arguments """

    global verbose

    parser = argparse.ArgumentParser()

    parser.add_argument('filename', help='image file that will be decorated')

    parser.add_argument('-c', '--compress', default=config.DEFAULT_COMPRESS_LEVEL, type=int,
                        help=('set compress level of output image. '
                              '(0 to 5, 0: highest compress, 5: no compress) '
                              '(default={})'.format(config.DEFAULT_COMPRESS_LEVEL)))

    parser.add_argument('-d', '--density', default=config.DEFAULT_DENSITY_LEVEL, type=int,
                        help=('set particles density. '
                              '(0 to 5, 0: most sparse, 5: most dense) '
                              '(default={})'.format(config.DEFAULT_DENSITY_LEVEL)))

    parser.add_argument('-f', '--frames', default=config.DEFAULT_N_FRAMES, type=int,
                        help=('set output image\'s number of frames '
                              '(default={})'.format(config.DEFAULT_N_FRAMES)))

    parser.add_argument('-p', '--particle', default=config.DEFAULT_PARTICLE_TYPE,
                        help=('set type of particle '
                              '(types: SNOW) '
                              '(default={})'.format(config.DEFAULT_PARTICLE_TYPE)))

    parser.add_argument('-s', '--speed', default=config.DEFAULT_SPEED_LEVEL, type=int,
                        help=('set particles speed. '
                              '(0 to 5, 0: slowest, 5: fastest) '
                              '(default={})'.format(config.DEFAULT_SPEED_LEVEL)))

    parser.add_argument('-S', '--size', default=config.DEFAULT_SIZE_LEVEL, type=int,
                        help=('set size of particle '
                              '(0 to 5, 0: smallest, 5: largest) '
                              '(default={})'.format(config.DEFAULT_SIZE_LEVEL)))

    parser.add_argument('-v', '--verbose', default=False, const=True, action='store_const',
                        help='print intermediate logs')

    parser.add_argument('-w', '--webp', default=False, const=True, action='store_const',
                        help='change output image format from gif to webp')

    parser.add_argument('--not_continuous', default=False, const=True, action='store_const',
                        help='output image becomes not continous')

    args = parser.parse_args()
    verbose = args.verbose

    settings = {
        'filename': args.filename,
        'frame_size': config.FRAME_SIZES[args.compress],
        'continuous': not args.not_continuous,
        'density': config.PARTICLE_NUMBERS[args.density] if args.not_continuous else config.LANE_NUMBERS[args.density],
        'n_frames': args.frames,
        'type': args.particle.upper(),
        'speed': config.SPEED_LEVELS[args.speed],
        'size': config.SIZE_LEVELS[args.size],
        'format': 'WEBP' if args.webp else 'GIF',
    }

    return settings


def log(string, force=False):
    if verbose or force:
        print('[*] {}'.format(string))


def main():

    args = parse_arguments()

    img = Image.open(args['filename'])
    log('Successfully opened image: {}'.format(args.get('filename')))

    if args['format'] == 'GIF':
        img = img.convert('P', palette=Image.ADAPTIVE, dither=Image.NONE)
    else:
        print("NOT IMPLEMENTED")
        exit(0)

    img_size = get_image_size(img)
    if img_size > args['frame_size']:
        img = resize_image(img, img_size, args['frame_size'])
        log('Compressed image to {}'.format(img.size))

    log('Starting decoration...')
    frames = decorators.decorate(img, args)
    log('Done decoration')

    # not sure why frames[0].save() not works properly...
    initial_frame = frames[0]
    initial_frame.save('out.{}'.format(args['format'].lower()), save_all=True, append_images=frames,
                       optimize=True, duration=30, loop=100)  # min duration : 20
    log('Saved image')

if __name__ == '__main__':
    main()