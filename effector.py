from PIL import Image
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


def snow(img, n_frames=50, n_particles=100, avr_speed=30, speed_deviation_level=1):
    size_x, size_y = img.size

    avr_particle_size = 6

    snow_particles = []
    for i in range(n_particles):
        snow_particles.append(Snow(max_x=size_x, max_y=size_y, size=avr_particle_size+random.randint(-2, 2)*2, speed_x=random.randint(-10, 10), speed_y=avr_speed+random.randint(-20,20)))

    frames = []
    for i in range(n_frames):

        frame = img.copy()
        pixels = frame.load()

        for p in snow_particles:

            px, py = p.get_position()
            sz = p.get_size()
            sz_half = sz // 2
            for x in range(-sz_half, sz_half+1):
                for y in range(-sz_half, sz_half+1):
                    xx = max(min(px+x, size_x-1), 0)
                    yy = max(min(py+y, size_y-1), 0)

                    if abs(xx-px)**2 + abs(yy-py)**2 < sz:
                        pixels[xx, yy] = p.color

            p.move()

        frames.append(frame)

    return frames


def main():
    filename = sys.argv[1]
    img = Image.open(filename)
    img = img.convert('P', palette=Image.ADAPTIVE)
    img_size = get_image_size(img)
    MAX_FRAME_SIZE = 128 * 10**3  # 128 kb

    if img_size > MAX_FRAME_SIZE:
        img = resize_image(img, img_size, MAX_FRAME_SIZE)

    frames = snow(img)

    img.save('out.gif', save_all=True, append_images=frames, optimize=True)


if __name__ == '__main__':
    main()