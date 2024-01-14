from PIL import Image
import colorsys
import math
import os

width = 1000 # pixels
x, y = -0.65, 0
x_range = 3.4
aspect_ratio = 4/3
max_iterations = 500

height = round(width / aspect_ratio)
y_range = x_range / aspect_ratio
min_x = x - x_range / 2
max_x = x + x_range / 2
min_y = y - y_range / 2
max_y = y + y_range / 2

img = Image.new('RGB', (width, height), color = 'black')
pixels = img.load()

def logColor(distance, base, const, scale):
    color = -1 * math.log(distance, base)
    rgb = colorsys.hsv_to_rgb(const + scale * color, 0.8, 0.9)
    return tuple(round(i * 255) for i in rgb)

def powerColor(distance, exp, const, scale):
    color = distance**exp
    rgb = colorsys.hsv_to_rgb(const + scale * color, 1 - 0.6 * color, 0.9)
    return tuple(round(i * 255) for i in rgb)
    

for row in range(height):
    for col in range(width):
        x = min_x + col * x_range / width
        y = max_y - row * y_range / height
        old_x = x
        old_y = y

        for i in range(max_iterations + 1):
            a = x**2 - y**2
            b = 2 * x * y
            x = a + old_x
            y = b + old_y
            if x**2 + y**2 > 4:
                break
        
        if i < max_iterations:
            distance = (i + 1) / (max_iterations + 1)
            rgb = logColor(distance, 0.2, 0.27, 1.0)
            pixels[col, row] = rgb
        index = row * width + col + 1
        print(f"{index} / {width * height}, {round(index / width / height * 100 * 10) / 10}%")

img.save('output.png')
os.system('feh output.png')