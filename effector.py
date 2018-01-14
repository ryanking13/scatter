from PIL import Image, ImageDraw
import sys
import math
from io import BytesIO
from particle import *


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


def snow(img, n_frames=50, n_particles=50, avr_speed=10, speed_deviation_level=1):

    avr_particle_size = 3

    snow_particles = []  # snow particle objects
    for i in range(n_particles):
        snow_particles.append(Snow(xy=img.size, size=avr_particle_size+random.randint(-2, 2)*2, speed_x=random.randint(-10, 10), speed_y=avr_speed+random.randint(-10, 10)))

    frames = []  # frames that will compose animated image
    for i in range(n_frames):

        frame = img.copy()
        effect_mask = Image.new('RGBA', img.size)  # image for masking
        draw_board = ImageDraw.Draw(effect_mask)

        for p in snow_particles:

            p.draw(draw_board)  # draw new particle
            p.move()

        frame.paste(effect_mask, mask=effect_mask)
        frames.append(frame)

    return frames


def main():

    filename = sys.argv[1]
    img = Image.open(filename)
    img = img.convert('P', palette=Image.ADAPTIVE)
    img_size = get_image_size(img)
    MAX_FRAME_SIZE = 256 * 10**3  # 256 kb

    if img_size > MAX_FRAME_SIZE:
        img = resize_image(img, img_size, MAX_FRAME_SIZE)

    frames = snow(img)

    img.save('out.gif', save_all=True, append_images=frames, optimize=True)


if __name__ == '__main__':
    main()