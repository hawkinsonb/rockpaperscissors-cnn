#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread
from skimage.transform import resize

# import all required lib
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread
from skimage.transform import resize


def visualize_input(img, ax):
    ax.imshow(img, cmap='gray')
    width, height = img.shape
    thresh = img.max()/2.5
    for x in range(width):
        for y in range(height):
            ax.annotate(str(round(img[x][y], 2)), xy=(y, x),
                        horizontalalignment='center',
                        verticalalignment='center',
                        color='white' if img[x][y] < thresh else 'black')


# Load a color image in grayscale
image = imread(
    '../data/resized/128/scissors/20190501_133143.jpg', as_grey=True)
image = resize(image, (128, 128), mode='reflect')

print('This image is: ', type(image),
      'with dimensions:', image.shape)

plt.imshow(image, cmap='gray')


fig = plt.figure(figsize=(16, 16))
ax = fig.add_subplot(111)
visualize_input(image, ax)


plt.show()
