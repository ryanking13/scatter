from PIL import Image, ImageDraw
import sys
import math
from io import BytesIO
from particle import *
from lane import ParticleLane

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


def snow_lane(img, n_lanes=40, n_frames=50, min_speed=(-2, 5), speed_deviation=(4, 3),
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

        for pos in positions:
            snow = Snow(
                xy=img.size,
                size=particle_size,
                speed_x=speed_x,
                speed_y=speed_y,
                position=pos
            )

            snow_particles.append(snow)

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


def snow(img, n_frames=50, n_particles=50, avr_speed=-10, speed_deviation_level=1):

    avr_particle_size = 3

    snow_particles = []  # snow particle objects
    for i in range(n_particles):
        snow_particles.append(Snow(xy=img.size, size=avr_particle_size+random.randint(-2, 2)*2, speed_x=random.randint(-5, 5), speed_y=avr_speed+random.randint(-10, 10)))

    frames = []  # frames that will compose animated image
    for i in range(n_frames):

        frame = img.copy()
        effect_mask = Image.new('RGBA', img.size)  # image for masking
        draw_board = ImageDraw.Draw(effect_mask)

        for p in snow_particles:

            p.draw(draw_board)  # draw new particle
            p.move()

        frame.paste(effect_mask, mask=effect_mask)
        # frame = frame.convert('P', Image.ADAPTIVE)
        frames.append(frame)

    return frames


def main():

    filename = sys.argv[1]
    img = Image.open(filename)
    # img = img.convert('P', palette=Image.ADAPTIVE)
    img_size = get_image_size(img)
    MAX_FRAME_SIZE = 256 * 10**3  # 256 kb

    if img_size > MAX_FRAME_SIZE:
        img = resize_image(img, img_size, MAX_FRAME_SIZE)

    frames = snow_lane(img)

    # not sure why frames[0].save() not works properly...
    initial_frame = frames[0]
    
    initial_frame.save('out.gif', save_all=True, append_images=frames, optimize=True, duration=1, palette=Image.ADAPTIVE)

if __name__ == '__main__':
    main()