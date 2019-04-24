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
<<<<<<< HEAD
image = imread('../data/resized/128/paper/2019-04-03_13-17-45_1.jpg', as_grey=True)
=======
image = imread('../data/resized/128/scissors/2019-04-03_13-17-35_1.jpg', as_gray=True)
>>>>>>> 26ffdf5485270eedc908f3ab0a5d7fff32ba4210
image = resize(image, (64, 64), mode='reflect')

print('This image is: ', type(image),
      'with dimensions:', image.shape)

plt.imshow(image, cmap='gray')


fig = plt.figure(figsize=(16, 16))
ax = fig.add_subplot(111)
visualize_input(image, ax)


plt.show()
