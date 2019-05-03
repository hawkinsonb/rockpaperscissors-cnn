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
input_shape = (num_channels, img_size, img_size)

classes = ['rock', 'paper', 'scissors']

train_path = '../data/augmented'
checkpoint_dir = "./saved_models"

validation_size = 0.5

# load image data and labels
data = pp.read_train_sets(train_path, img_size, classes,
                          validation_size=validation_size)

x_train, y_train = data.train._images, data.train._labels
x_valid, y_valid = data.valid._images, data.valid._labels

# split validation into training and validation sets
x_test, y_test = x_valid[:1000], y_valid[:1000]
x_valid, y_valid = x_valid[1000:], y_valid[1000:]

filepath = "saved_models/rps.h5"
checkpoint = ModelCheckpoint(
    filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

# define the model
model = Sequential()

model.add(Conv2D(filters=2, kernel_size=(3, 3),
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=4, kernel_size=(3, 3),
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=8, kernel_size=(3, 3),
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.3))
model.add(Conv2D(filters=16, kernel_size=(3, 3),
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=20, kernel_size=(3, 3),
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=32, kernel_size=(3, 3),
                 padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dense(3, activation='softmax'))

opt = keras.optimizers.RMSprop(lr=1e-04, decay=1e-6)
#opt2_ = keras.optimizers.SGD(lr=1e-04)
# old_opt = keras.optimizers.RMSprop(lr=1e-04);
model.compile(loss='categorical_crossentropy',
              optimizer=opt, metrics=['accuracy'])

filepath = "saved_models/rps.h5"
checkpoint = ModelCheckpoint(
    filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

if (os.path.isfile(filepath)):
    model.load_weights(filepath)
    loss, acc = model.evaluate(x_train, y_train)
    print("Restored model, accuracy: {:5.2f}%".format(100*acc))

# train the model
model.fit(x_train, y_train, batch_size=2048, epochs=1000,
          validation_data=(x_valid, y_valid), verbose=1, shuffle=True, callbacks=callbacks_list)

# Save model and weights
save_dir = os.path.join(os.getcwd(), checkpoint_dir)
model_name = 'rps.h5'
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)
model_path = os.path.join(save_dir, model_name)
model.save(model_path)
print('Saved trained model at %s ' % model_path)

# test and display results
score = model.evaluate(x_test, y_test, batch_size=128, verbose=1)
print('Test score:', score[0])
print('Test accuracy:', score[1])
