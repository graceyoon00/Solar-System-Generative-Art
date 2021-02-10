# cario for vector art, argparse for command-line options
import cairo, PIL, argparse, math, random
#PIL for grainy effect
from PIL import Image, ImageDraw

color_lib = [(217, 48, 48), (255, 110, 25), (255, 185, 71), (255, 201, 25), (113, 156, 6), 
(67, 171, 2), (69, 196, 120), (45, 173, 131), (33, 191, 189), (34, 148, 214),
(31, 79, 209), (108, 31, 209), (191, 34, 212), (212, 34, 141)]

border_lib = [(234, 204, 255), (255, 255, 255), (255, 251, 171), (207, 207, 207), (173, 203, 255)]

float_gen = lambda a, b: random.uniform(a, b)

def make_orbit(cr, line, x, y, radius, r, g, b):
    cr.set_line_width(line)
    cr.arc(x, y, radius, 0, 2*math.pi)
    cr.stroke()

#centered by default
def planet_fill(cr, x, y, radius, r, g, b):
    cr.set_source_rgb(r, g, b)
    cr.arc(x, y, radius, 0, 2*math.pi)
    cr.fill()

def make_border(cr, size, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, size, height)
    cr.rectangle(0, 0, width, size)
    cr.rectangle(0, height-size, width, size)
    cr.rectangle(width-size, 0, size, height)
    cr.fill()

def make_background(cr, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, width, height) #draw and fill rectangle
    cr.fill()

def main():
    parser = argparse.ArgumentParser()
    # width and height settings
    parser.add_argument("-wi", "--width", help="Specify Width", default=3000, type=int)
    parser.add_argument("-he", "--height", help="Specify Height", default=2000, type=int)
    # line style (orbit/curved or straight line)
    parser.add_argument("-o", "--orbit", help="Actual Orbits", action="store_true")
    parser.add_argument("-sl", "--line", help=".", action="store_true")
    # center planet and border size 
    parser.add_argument("-sun", "--sunsize", help=".", default=random.randint(200, 400), type=int)
    parser.add_argument("-bs", "--bordersize", help=".", default=50, type=int)
    # set noise to 0 for smooth texture
    parser.add_argument("-n", "--noise", help="Texture", default=.4, type=float)
    args = parser.parse_args()

    #size/image settings
    width, height = args.width, args.height
    border_size = args.bordersize
    sun_size = args.sunsize

    sun_center = height - border_size

    img_set = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(img_set)

    #background and other colour settings
    make_background(cr, 0, 0, 0, width, height)

    sun_color = random.choice(color_lib)
    sun_r, sun_g, sun_b = sun_color[0]/255.0, sun_color[1]/255.0, sun_color[2]/255.0

    planet_fill(cr, width/2, sun_center, sun_size, sun_r, sun_g, sun_b)
    distance_between_planets = 20
    center_prev = sun_center
    size_prev = sun_size
    color_prev = sun_color

    min_size = 5
    max_size = 60

    for i in range(1, 20):
        next_size = random.randint(min_size, max_size)
        next_center = center_prev - size_prev - (next_size * 2) - distance_between_planets

        if not(next_center - next_size < border_size):
            if(args.orbit):
                make_orbit(cr, 4, width/2, sun_center, height - next_center - border_size, .6, .6, .6)
            elif(args.line):
                cr.move_to(border_size * 2, next_center)
                cr.line_to(width-(border_size*2), next_center)
                cr.stroke()

            rand_color = random.choice(color_lib)
            while (rand_color is color_prev):
                rand_color = random.choice(color_lib)

            color_prev = rand_color

            r, g, b = rand_color[0]/255.0, rand_color[1]/255.0, rand_color[2]/255.0

            planet_fill(cr, width/2, next_center, next_size, r, g, b)

            center_prev = next_center
            size_prev = next_size

            min_size += 5
            max_size += 5 * i

    border_color = random.choice(border_lib)
    bord_r, bord_g, bord_b = border_color[0]/255.0, border_color[1]/255.0, border_color[2]/255.0
    make_border(cr, border_size, bord_r, bord_g, bord_b, width, height)

    #image output
    img_set.write_to_png('Generative-Output.png')
    pil_image = Image.open('Generative-Output.png')
    pixels = pil_image.load()

    for i in range(pil_image.size[0]):
        for j in range(pil_image.size[1]):
            r, g, b = pixels[i, j]

            noise = float_gen(1.0 - args.noise, 1.0 + args.noise)
            pixels[i, j] = (int(r*noise), int(g*noise), int(b*noise))
    pil_image.save('Generative-Output.png')

if __name__ == "__main__":
    main()