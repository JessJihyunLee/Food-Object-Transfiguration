"""
Some codes from https://github.com/Newmu/dcgan_code
"""
from __future__ import division
import math
import pprint
import scipy.misc
import numpy as np
import os
from time import gmtime, strftime

pp = pprint.PrettyPrinter()

get_stddev = lambda x, k_h, k_w: 1 / math.sqrt(k_w * k_h * x.get_shape()[-1])

def load_data_pair(image_path, flip=False, is_test=False, img_size=256):
    img_A, img_B = load_image_pair(image_path)
    img_A, img_B = preprocess_A_and_B(img_A, img_B, img_size=img_size)

    img_A = img_A / 127.5 - 1.
    img_B = img_B / 127.5 - 1.
    if len(img_A.shape) < 3:
        img_A = np.expand_dims(img_A, axis=2)
        img_B = np.expand_dims(img_B, axis=2)
    img_AB = np.concatenate((img_A, img_B), axis=2)
    return img_AB


def load_image_pair(image_path):
    input_img = imread(image_path)
    w = int(input_img.shape[1])
    w2 = int(w / 2)
    img_A = input_img[:, 0:w2]
    img_B = input_img[:, w2:w]

    return img_A, img_B


def preprocess_A_and_B(img_A, img_B, img_size=256):
    img_A = scipy.misc.imresize(img_A, [img_size, img_size])
    img_B = scipy.misc.imresize(img_B, [img_size, img_size])
    return img_A, img_B


def load_data(image_path, flip=False, is_test=False, image_size=128):
    img = load_image(image_path)
    img = preprocess_img(img, img_size=image_size, flip=flip, is_test=is_test)

    img = img / 127.5 - 1.
    if len(img.shape) < 3:
        img = np.expand_dims(img, axis=2)
    return img


def load_image(image_path):
    img = imread(image_path)
    return img


def preprocess_img(img, img_size=128, flip=False, is_test=False):
    img = scipy.misc.imresize(img, [img_size, img_size])
    if (not is_test) and flip and np.random.random() > 0.5:
        img = np.fliplr(img)
    return img

def save_images(images, size, image_path):
    dir = os.path.dirname(image_path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    return imsave(inverse_transform(images), size, image_path)


def imread(path, is_grayscale=False):
    if (is_grayscale):
        return scipy.misc.imread(path, flatten=True)  # .astype(np.float)
    else:
        return scipy.misc.imread(path)  # .astype(np.float)


def merge_images(images, size):
    return inverse_transform(images)


def merge(images, size):
    h, w = images.shape[1], images.shape[2]
    if len(images.shape) < 4:
        img = np.zeros((h * size[0], w * size[1], 1))
        images = np.expand_dims(images, axis=3)
    else:
        img = np.zeros((h * size[0], w * size[1], images.shape[3]))
    for idx, image in enumerate(images):
        i = idx % size[1]
        j = idx // size[1]
        img[j * h:j * h + h, i * w:i * w + w, :] = image
    if images.shape[3] == 1:
        return np.concatenate([img, img, img], axis=2)
    else:
        return img.astype(np.uint8)


def imsave(images, size, path):
    return scipy.misc.imsave(path, merge(images, size))


def inverse_transform(images):
    return ((images + 1.) * 127.5)  # /2.