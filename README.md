# Image Decorator

Add some beautiful & animated decoration on your image!

Inspired from [Your Lie in April Ep. 22](https://i.pinimg.com/originals/94/0b/7a/940b7a47dc5abacd4734d4c6e2ca822f.gif)

## Requirements

- Python 3.x
- [Pillow](https://github.com/python-pillow/Pillow)

```
$ pip install Pillow
```

## Usage

```
usage: run.py [-h] [-c COMPRESS] [-d DENSITY] [-f FRAMES] [-p PARTICLE]
              [-P PALETTE] [-s SPEED] [-S SIZE] [-v] [-w] [--not_continuous]
              filename

positional arguments:
  filename              image file that will be decorated

optional arguments:
  -h, --help            show this help message and exit
  -c COMPRESS, --compress COMPRESS
                        set compress level of output image. (0 to 5, 0:
                        highest compress, 5: no compress) (default=3)
  -d DENSITY, --density DENSITY
                        set particles density. (0 to 5, 0: most sparse, 5:
                        most dense) (default=3)
  -f FRAMES, --frames FRAMES
                        set output image's number of frames (default=50)
  -p PARTICLE, --particle PARTICLE
                        set type of particle (types: SNOW) (default=SNOW)
  -P PALETTE, --palette PALETTE
                        set color palette (types: BRIGHT, DAWN, PINK, WHITE)
                        (default=WHITE)
  -s SPEED, --speed SPEED
                        set particles speed. (0 to 5, 0: slowest, 5: fastest)
                        (default=3)
  -S SIZE, --size SIZE  set size of particle (0 to 5, 0: smallest, 5: largest)
                        (default=3)
  -v, --verbose         print intermediate logs
  -w, --webp            change output image format from gif to webp
  --not_continuous      output image becomes not continous
```

## Sample

<img src="./sample/sample.gif" width=697 height=435 />

<br>

<img src="./sample/sample2.gif" width=697 height=435 />

## TODO

1. Adding decoration types
1. Fixing particle color changing problem
1. Optimizing decoration time
1. WEBP support
1. Solve PNG time problem
1. Adding more user-controlled parameters
1. Adding more color palettes

## CHANGELOG

- 2018-01-23: Add public usage and attached LICENSE
