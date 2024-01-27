from PIL import Image
import sys
import numpy as np

imglink = sys.argv[1]

image = Image.open(imglink)

def find_nearest_color(col):
    return np.round(col / 255)

def apply_convolution(img, n):
#    square = min(round(img.height / n), round(img.width / n))
    image = np.array(img, dtype=float)

    new_img = np.empty((round(img.height / n), round(img.width / n)), dtype=np.uint8)
    for i in range(0, img.height, n):
        for j in range(0, img.width, n):
            try:
                pixvals = [image[i + y][j + x] for y in range(n) for x in range(n)]
                avg = round(np.mean(pixvals))
                new_img[i][j] = avg
            except:
                pass

    Image.fromarray(new_img.astype(np.uint8)).show()

    return new_img


def floyd_steinberg(img, n):
    image = np.array(img, dtype=float)
    notreal = apply_convolution(img, n)
    copy = image.copy()

    for i in range(img.height):
        for j in range(img.width):

            old_val = copy[i][j]
            new_val = find_nearest_color(image[i][j])
            image[i][j] = new_val

            error = new_val - old_val

            try:
                image[i][j-1] = old_val + error * 3/16
            except:
                pass

            try:
                image[i+1][j] = old_val + error * 5/16
            except:
                pass

            try:
                image[i][j+1] = old_val + error * 7/16
                image[i+1][j+1] = old_val + error * 1/16 
            except:
                pass

    return Image.fromarray(image.astype(np.uint8)) 

image = floyd_steinberg(image, 2)
image.show()
