import numpy.fft
import numpy as np
import scipy.ndimage.filters as filters

from itertools import product
from PIL import Image, ImageFilter

from goscore.efficient import transform


def image_to_numpy_contour(im, scale):
    im = im.resize((im.size[0]//scale, im.size[1]//scale), Image.BICUBIC)
    contours = im.filter(ImageFilter.CONTOUR).convert("L")
    arr = 255-np.array(contours)

    arr[0,:]  = 0
    arr[-1,:] = 0
    arr[:,0]  = 0
    arr[:,-1] = 0

    arr = arr.astype(np.float64)
    arr = arr - arr.min()
    arr /= arr.max()
    arr *= 255
    return arr

def transform_inefficient(inp, oshape):
    max_radius = np.sqrt(inp.shape[0]*inp.shape[0] + inp.shape[1]*inp.shape[1])
    out = np.zeros(oshape)
    sin_a = np.zeros(oshape[0])
    cos_a = np.zeros(oshape[0])
    for angle in range(oshape[0]):
        sin_a[angle] = np.sin(2*np.pi*(angle/oshape[0]))
        cos_a[angle] = np.cos(2*np.pi*(angle/oshape[0]))

    for(x,y) in product(range(inp.shape[0]), range(inp.shape[1])):
        if inp[x,y] < 10:
            continue
        for angle in range(oshape[0]):
            radius = sin_a[angle]*x + cos_a[angle]*y
            radius = (radius/(2 * max_radius)) + 0.5
            output_r = int(oshape[1]*radius)
            if 0 <= output_r <= oshape[1] - 1:
                out[angle, output_r] += inp[x, y]
    return out


def draw_line(image, oshape, angle, radius):
    max_radius = np.sqrt(image.shape[0]*image.shape[0] + image.shape[1]*image.shape[1])
    sin_a = np.sin(2*np.pi * (angle/oshape[0]))
    cos_a = np.cos(2*np.pi * (angle/oshape[0]))
    r = (radius/oshape[1] - 0.5)*2*max_radius
    for x in range(image.shape[0]):
        t0 = int((r - (x-1)*sin_a)/cos_a)
        t1 = int((r - x*sin_a)/cos_a)
        tmin = max(0, min(t0, t1))
        tmax = min(image.shape[1]-1, max(t0, t1) + 1)
        for y in range(tmin, tmax+1):
            image[x,y] = 255
