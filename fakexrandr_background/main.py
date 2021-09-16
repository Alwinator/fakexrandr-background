import os
import random
import tempfile
import time
import logging
import argparse
from pathlib import Path

import cv2
import numpy as np

from screen import get_screen

parser = argparse.ArgumentParser(description='fakexrandr-background')
parser.add_argument('picture_folder', type=Path, help='The path to your picture folder.')
parser.add_argument('change_duration', type=float, help='The duration to wait between every picture change. '
                                                        '(In seconds)')
parser.add_argument('--delay', type=float, default=0, help='A delay at the beginning. Linux often needs some time to '
                                                           'setup the displays after startup. (In seconds)')

args = parser.parse_args()
logging.basicConfig(level=logging.INFO)


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


def main():
    logging.info("Starting...")

    logging.info(f"Waiting {args.delay} seconds")
    time.sleep(args.delay)

    logging.info("Get xrandr displays")
    screen = get_screen()

    logging.info("Get picture paths")
    picture_paths = get_paths(args.picture_folder)

    logging.info("Set gsettings set org.gnome.desktop.background picture-options to spanned")
    os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-options 'spanned'")

    while True:
        logging.info("Generating picture...")
        background = create_picture(screen, picture_paths)

        with tempfile.NamedTemporaryFile() as tmp:
            cv2.imwrite(tmp.name + ".jpg", background)
            logging.info("Picture saved")

            os.system(f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri file:///{tmp.name}.jpg")
            logging.info("Background updated")

        logging.info(f"Waiting for {args.change_duration} seconds")
        time.sleep(args.change_duration)


if __name__ == '__main__':
    main()
