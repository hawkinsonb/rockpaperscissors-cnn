#!/usr/bin/env python3
import os
import keras
import numpy as np
import matplotlib.pyplot as plt

import Preprocessor as pp

from keras.utils import np_utils
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.callbacks import ModelCheckpoint

num_channels = 3
img_size = 128
input_shape = (img_size, img_size, num_channels)

classes = ['rock', 'paper', 'scissors']

train_path = '../data/resized/' + str(img_size)
checkpoint_dir = "./saved_models"

validation_size = 0.15

# load image data and labels
data = pp.read_train_sets(train_path, img_size, classes,
                          validation_size=validation_size)

x_train, y_train = data.train._images, data.train._labels
x_valid, y_valid = data.valid._images, data.valid._labels

# split validation into training and validation sets
x_test, y_test = x_valid[:50], y_valid[:50]
x_valid, y_valid = x_valid[50:], y_valid[50:]

# define the model
model = Sequential()
model.add(Conv2D(filters=16, kernel_size=(3,3), padding='same', activation='relu',
                 input_shape=input_shape))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=32, kernel_size=(3,3),
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=64, kernel_size=(3,3),
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=128, kernel_size=(3,3),
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=256, kernel_size=(3,3),
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=512, kernel_size=(3,3),
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=1024, kernel_size=(3,3),
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))

model.add(Dropout(0.4))
model.add(Flatten())
model.add(Dropout(0.6))
model.add(Dense(512, activation='relu'))
model.add(Dense(3, activation='softmax'))

opt = keras.optimizers.RMSprop(lr=1e-04, decay=1e-6)
#opt2_ = keras.optimizers.SGD(lr=1e-04)
# old_opt = keras.optimizers.RMSprop(lr=1e-04);
model.compile(loss='categorical_crossentropy',
              optimizer=opt, metrics=['accuracy'])

filepath = "saved_models/rps-flow.h5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

# train the model
model.fit(x_train, y_train, batch_size=32, epochs=30,
          validation_data=(x_valid, y_valid), verbose=1, shuffle=True)

# Save model and weights
save_dir = os.path.join(os.getcwd(), checkpoint_dir)
model_name = 'rps.h5'
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)
model_path = os.path.join(save_dir, model_name)
model.save(model_path)
print('Saved trained model at %s ' % model_path)

# test and display results
score = model.evaluate(x_test, y_test, batch_size=32, verbose=1)
print('Test score:', score[0])
print('Test accuracy:', score[1])