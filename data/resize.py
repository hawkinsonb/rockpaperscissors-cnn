#!/usr/bin/env python3

import glob
import os

from PIL import Image

def apply_augmentations(image):
    pass

def resize(size):
    classes = ['rock', 'paper', 'scissors']

    # change relatives after debug
    read_root = '../data/rps'
    save_root = '../data/resized/128'
    
    for fld in classes:
        fld_save_path = os.path.join(save_root, fld)
        print(fld_save_path)
        fld_read_path = os.path.join(read_root, fld, '*g')
        print(fld_read_path)
        files = glob.glob(fld_read_path)

        for fl in files:
            fl_save_path = os.path.join(fld_save_path, os.path.basename(fl))

            image = Image.open(fl).convert('RGB')
            image = image.resize((size, size))

            image.save(fl_save_path)

# Resizing image to size 128
resize(128)