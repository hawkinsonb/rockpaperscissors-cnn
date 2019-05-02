#!/usr/bin/env python3

import os
import keras

import numpy as np
import matplotlib.pyplot as plt

from keras.utils import np_utils
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.callbacks import ModelCheckpoint


num_channels = 3
img_size = 128
batch_size = 32
_epochs = 30

input_shape = (img_size, img_size, num_channels)

classes = ['rock', 'paper', 'scissors']

train_path = '../data/resized/' + str(img_size)
checkpoint_dir = "./saved_models"


# pp.plot_images(images,img_size, num_channels, cls_true)

datagen_args = dict(rotation_range=90,
                    # width_shift_range=0.1,
                    # height_shift_range=0.1,
                    rescale=1./255,
                    # zoom_range=0.2,
                    # shear_range=0.1,
                    brightness_range=(1.0, 1.5),
                    validation_split=0.25,
                    horizontal_flip=True,
                    vertical_flip=True)

flow_args = dict(color_mode='rgb',
                 classes=classes,
                 target_size=(img_size, img_size),
                 batch_size=batch_size,
                 class_mode='categorical')

train_datagen = ImageDataGenerator(**datagen_args)

train_flow = train_datagen.flow_from_directory(
    train_path, subset='training', **flow_args)
validation_flow = train_datagen.flow_from_directory(
    train_path, subset='validation', **flow_args)

steps_per_epoch = len(train_flow.filenames) // batch_size
validation_steps = len(validation_flow.filenames) // batch_size

# define the model
model = Sequential()
model.add(Conv2D(filters=16, kernel_size=2, padding='same', activation='relu',
                 input_shape=input_shape))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=32, kernel_size=2,
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=64, kernel_size=2,
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=128, kernel_size=2,
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=256, kernel_size=2,
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dropout(0.4))
model.add(Dense(500, activation='relu'))
model.add(Dense(3, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop', metrics=['accuracy'])

filepath = "saved_models/rps-flow.h5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model.fit_generator(generator=train_flow, validation_data=validation_flow,
                    validation_steps=validation_steps, steps_per_epoch=steps_per_epoch, epochs=_epochs, callbacks=callbacks_list)

# Save model and weights
save_dir = os.path.join(os.getcwd(), 'saved_models')
model_name = 'rps-flow.h5'
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)

model_path = os.path.join(save_dir, model_name)
model.save(model_path)
print('Saved trained model at %s' % model_path)
