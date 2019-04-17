#!/usr/bin/env python3

# CNN for cifar-10 set
# tested in Anaconda environment

import os
import numpy as np
import matplotlib.pyplot as plt

import keras
from keras.datasets import cifar10
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, AveragePooling2D

# load the cifar10 data
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# slice data into training and validation sets
(x_train, x_valid) = x_train[5000:], x_train[:5000]
(y_train, y_valid) = y_train[5000:], y_train[:5000]

# normalize training and test data
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# one-hot encode labels
num_classes = len(np.unique(y_train))
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# define the model
model = Sequential()
model.add(Conv2D(filters=16, kernel_size=2, padding='same', activation='relu', 
                        input_shape=(32, 32, 3)))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=32, kernel_size=2, padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=64, kernel_size=2, padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))


model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(500, activation='relu'))

# final layer - fully connected and results in a probability for each of
# of the ten classes
model.add(Dense(10, activation='softmax'))


# Save model and weights
save_dir = os.path.join(os.getcwd(), 'saved_models')
model_name = 'keras_cifar10_trained_model.h5'
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)
model_path = os.path.join(save_dir, model_name)
model.save(model_path)
print('Saved trained model at %s ' % model_path)

# compile and train model
model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=32, epochs=8)

# test and display results
score = model.evaluate(x_test, y_test, batch_size=32, verbose=1)
print('Test score:', score[0])
print('Test accuracy:', score[1])
