import os
import random
from pathlib import Path

import cv2
import numpy as np


# From https://stackoverflow.com/a/58034691/6760875
def crop_and_resize(img, w, h):
    im_h, im_w, channels = img.shape
    res_aspect_ratio = w / h
    input_aspect_ratio = im_w / im_h

    if input_aspect_ratio > res_aspect_ratio:
        im_w_r = int(input_aspect_ratio * h)
        im_h_r = h
        img = cv2.resize(img, (im_w_r, im_h_r))
        x1 = int((im_w_r - w) / 2)
        x2 = x1 + w
        img = img[:, x1:x2, :]
    if input_aspect_ratio < res_aspect_ratio:
        im_w_r = w
        im_h_r = int(w / input_aspect_ratio)
        img = cv2.resize(img, (im_w_r, im_h_r))
        y1 = int((im_h_r - h) / 2)
        y2 = y1 + h
        img = img[y1:y2, :, :]
    if input_aspect_ratio == res_aspect_ratio:
        img = cv2.resize(img, (w, h))

    return img


def create_picture(screen, picture_paths):
    background = np.zeros((screen.height, screen.width, 3), np.uint8)
    chosen_paths = random.sample(picture_paths, len(screen.displays))

    for i, display in enumerate(screen.displays):
        img = cv2.imread(str(chosen_paths[i]))
        img = crop_and_resize(img, display.width, display.height)
        background[display.top:display.top + display.height, display.left:display.left + display.width] = img

    return background


def get_paths(picture_path):
    pictures = os.listdir(picture_path)
    pictures = map(lambda path: picture_path / Path(path), pictures)
    pictures = filter(lambda path: path.is_file(), pictures)
    pictures = filter(lambda path:
                      path.name.endswith(".png") or
                      path.name.endswith(".jpg") or
                      path.name.endswith(".jpeg"), pictures)
    return list(pictures)