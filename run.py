import argparse
from PIL import Image
import config
import decorators
from functions import *
import logger


def parse_arguments():
    """ parse command line arguments """

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

    parser.add_argument('-P', '--palette', default=config.DEFAULT_COLOR_PALETTE,
                        help=('set color palette '
                              '(types: BRIGHT, DAWN, PINK, WHITE) '
                              '(default={})'.format(config.DEFAULT_COLOR_PALETTE)))

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

    parser.add_argument('-w', '--webp', default='GIF', const='WEBP', dest='format', action='store_const',
                        help='change output image format from gif to webp')

    parser.add_argument('-o', '--output', default=config.DEFAULT_OUTPUT_NAME,
                        help=('set output file name '
                              '(default={})'.format(config.DEFAULT_OUTPUT_NAME)))
    # not implemented
    parser.add_argument('--not_continuous', default=False, const=True, action='store_const',
                        help='output image becomes not continous')

    args = parser.parse_args()
    if args.verbose:
        logger.set_verbose()

    settings = {
        'filename': args.filename,
        'frame_size': config.FRAME_SIZES[args.compress],
        'continuous': not args.not_continuous,
        'density': config.PARTICLE_NUMBERS[args.density] if args.not_continuous else config.LANE_NUMBERS[args.density],
        'n_frames': args.frames,
        'type': args.particle.upper(),
        'palette': args.palette.upper(),
        'speed': config.SPEED_LEVELS[args.speed],
        'size': config.SIZE_LEVELS[args.size],
        'format': args.format,
        'outputname': args.output if '.' in args.output else args.output + '.' + args.format.lower()
    }

    return settings


def main():

    args = parse_arguments()

    img = Image.open(args['filename'])
    logger.log('[*] Successfully opened image: {}'.format(args.get('filename').split('/')[-1]))

    if args['format'] == 'GIF':
        img = img.convert('P', palette=Image.ADAPTIVE, dither=Image.NONE)

    img_size = get_image_size(img)
    if img_size > args['frame_size']:
        img = resize_image(img, img_size, args['frame_size'])
        logger.log('[*] Compressed image to {}'.format(img.size))

    logger.log('[*] Starting decoration...')
    frames = decorators.decorate(img, args)
    logger.log('[*] Done decoration')

    # not sure why frames[0].save() not works properly...
    initial_frame = frames[0]
    initial_frame.save(args['outputname'], save_all=True, append_images=frames,
                       optimize=True, duration=30, loop=0xffff)  # min duration : 20
    logger.log('[*] Saved image to - {}'.format(args['outputname']))

if __name__ == '__main__':
    main()