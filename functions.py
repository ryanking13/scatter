from io import BytesIO
import math
from PIL import Image


def generate_weighted_list(st, ed, ratio=(20, 2, 1)):

    """
    Generate an integer list consists of [st, ed].
    Ratio of each integer in the list is determined using ratio parameter.

    For example, st = 1, ed = 6, ratio = (20, 2, 1),
    output = [ 20 1s, 20 2s, 2 3s, 2 4s, 1 5s, 1 6s ]
    """

    nums = [i for i in range(st, ed+1)]

    n_boundary = len(ratio)
    boundary_offset = (ed - st + n_boundary) // n_boundary

    choices = []
    for i, n in enumerate(nums):
        r = ratio[i // boundary_offset]
        choices.extend([n] * r)

    return choices


def get_image_size(image):

    """ Calculate the size(bytes) of the image """

    tp_file = BytesIO()
    image.save(tp_file, 'GIF')

    return tp_file.tell()


def resize_image(img, cur_size, target_size):

    """
    Compress image by shrinking it.

    cur_size is the original images size(bytes).
    target_size is the resized images size(bytes).

    This function works by heuristic, so resized image's size is not exactly target_size.
    """
    if cur_size <= target_size:
        return img

    shrink_ratio = target_size / cur_size
    side_ratio = math.sqrt(shrink_ratio)

    x, y = img.size
    x_ = int(x * side_ratio)
    y_ = int(y * side_ratio)
    return img.resize((x_, y_), Image.ANTIALIAS)