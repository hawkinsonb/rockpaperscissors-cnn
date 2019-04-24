#!/usr/bin/env python3

import tensorflow as tf 

def convert(h5_file):
    converter = tf.lite.TFLiteConverter.from_keras_model_file(h5_file)
    tflite_model = converter.convert()
    with open('./saved_models/converted_model.tflite', 'wb') as converted:
         converted.write(tflite_model)

if __name__ == '__main__':
    convert('./saved_models/rps.h5')