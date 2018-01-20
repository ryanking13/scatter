from PIL import Image, ImageDraw
import sys
import math
from io import BytesIO
from particle import *
from lane import ParticleLane
import color_palette


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


def snow_lane(img, n_lanes=40, n_frames=50, min_speed=(-2, 2), speed_deviation=(4, 3),
              min_particle_size=3, particle_size_deviation=2):

    lanes = []
    for i in range(n_lanes):
        position = (random.randint(0, img.size[0]), random.randint(0, img.size[1]))
        speed_x = min_speed[0] + random.randint(0, speed_deviation[0])
        speed_y = min_speed[1] + random.randint(0, speed_deviation[1])
        size = min_particle_size + random.randint(0, particle_size_deviation)

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

    filename = sys.argv[1]
    img = Image.open(filename)
    img = img.convert('P', palette=Image.ADAPTIVE, dither=Image.NONE)
    img_size = get_image_size(img)
    MAX_FRAME_SIZE = 256 * 10**3  # 256 kb

    if img_size > MAX_FRAME_SIZE:
        img = resize_image(img, img_size, MAX_FRAME_SIZE)

    frames = snow_lane(img)

    # not sure why frames[0].save() not works properly...
    initial_frame = frames[0]
    initial_frame.save('out.gif', save_all=True, append_images=frames, optimize=True, duration=30)  # min duration : 20

if __name__ == '__main__':
    main()