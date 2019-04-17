#!/usr/bin/env python3

import glob
import time
import random
import os

import matplotlib.pyplot as plt
import numpy as np

from skimage.transform import resize
from skimage.io import imread

from keras.preprocessing.image import ImageDataGenerator


class DataSet:
    def __init__(self, images, labels, ids, cls):
        self._images = images
        self._labels = labels
        self._ids = ids
        self._cls = cls

        self._num_examples = len(images)
        self._index_in_epoch = 0
        self._epochs_completed = 0

    def next_batch(self, batch_size):
        '''Return the next `batch_size` examples from this data set.'''
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch
        return self._images[start:end], self._labels[start:end], self._ids[start:end], self._cls[start:end]


class DataSets:
    pass


def load_train(train_path, image_size, classes):
    images = []
    labels = []
    ids = []
    cls = []

    print('Reading training images')
    for fld in classes:
        index = classes.index(fld)
        print(f'Loading {fld} files (Index: {index})')
        path = os.path.join(train_path, fld, '*g')
        files = glob.glob(path)
        for fl in files:
            image = imread(fl)
            image = image[:, :, :3]
            image = resize(image, (image_size, image_size))
            images.append(image)
            label = np.zeros(len(classes))
            label[index] = 1.0
            labels.append(label)
            flbase = os.path.basename(fl)
            ids.append(flbase)
            cls.append(fld)
    images = np.array(images)
    labels = np.array(labels)

    images, labels = shuffle(images, labels)
    ids = np.array(ids)
    cls = np.array(cls)
    return images, labels, ids, cls


def shuffle(images, labels):
    assert len(images) == len(labels)
    p = np.random.permutation(len(images))
    return images[p], labels[p]


def load_test(test_path, image_size):
    path = os.path.join(test_path, '*g')
    files = sorted(glob.glob(path))

    X_test = []
    X_test_id = []
    print("Reading test images")
    for fl in files:
        flbase = os.path.basename(fl)
        img = plt.imread(fl)
        img = resize(img, (image_size, image_size))
        X_test.append(img)
        X_test_id.append(flbase)
    X_test = np.array(X_test, dtype=np.uint8)
    X_test = X_test.astype('float32')
    X_test = X_test / 255
    return X_test, X_test_id


def read_test_set(test_path, image_size):
    images, ids = load_test(test_path, image_size)
    return images, ids


def read_train_sets(train_path, image_size, classes, validation_size=0):
    data_sets = DataSets()
    images, labels, ids, cls = load_train(train_path, image_size, classes)
    # images, labels, ids, cls = shuffle(images, labels, ids, cls)

    if isinstance(validation_size, float):
        validation_size = int(validation_size * images.shape[0])
        validation_images = images[:validation_size]
        validation_labels = labels[:validation_size]
        validation_ids = ids[:validation_size]
        validation_cls = cls[:validation_size]
        train_images = images[validation_size:]
        train_labels = labels[validation_size:]
        train_ids = ids[validation_size:]
        train_cls = cls[validation_size:]
        data_sets.train = DataSet(
            train_images, train_labels, train_ids, train_cls)
        data_sets.valid = DataSet(
            validation_images, validation_labels, validation_ids, validation_cls)
    return data_sets


def plot_images(images, img_size, num_channels, cls_true, cls_pred=None):
    if len(images) == 0:
        print("no images to show")
        return
    else:
        random_indices = random.sample(range(len(images)), min(len(images), 9))
        images, cls_true = zip(*[(images[i], cls_true[i])
                                 for i in random_indices])
    fig, axes = plt.subplots(3, 3)
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    for i, ax in enumerate(axes.flat):
        # Plot image.
        ax.imshow(images[i])
        if cls_pred is None:
            xlabel = "True: {0}".format(cls_true[i])
        else:
            xlabel = "True: {0}, Pred: {1}".format(cls_true[i], cls_pred[i])
        ax.set_xlabel(xlabel)
        ax.set_xticks([])
        ax.set_yticks([])
    plt.show()
