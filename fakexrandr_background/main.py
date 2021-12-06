import threading
import time
import logging
import argparse
from pathlib import Path

from fakexrandr_background.gsetting_actions import update_picture, set_spanned
from fakexrandr_background.icon import show_icon
from fakexrandr_background.picture_utils import get_paths
from screen import get_screen

parser = argparse.ArgumentParser(description='fakexrandr-background')
parser.add_argument('picture_folder', type=Path, help='The path to your picture folder.')
parser.add_argument('change_duration', type=float, help='The duration to wait between every picture change. '
                                                        '(In seconds)')
parser.add_argument('--delay', type=float, default=0, help='A delay at the beginning. Linux often needs some time to '
                                                           'setup the displays after startup. (In seconds)')
parser.add_argument('--brightness', type=float, default=1, help='A value between 0 and 1 to set dim the background')

args = parser.parse_args()
logging.basicConfig(level=logging.INFO)


def loop(screen, picture_paths):
    set_spanned()

    while True:
        update_picture(screen, picture_paths, args.brightness)

        logging.info(f"Waiting for {args.change_duration} seconds")
        time.sleep(args.change_duration)


def main():
    logging.info("Starting...")

    logging.info(f"Waiting {args.delay} seconds")
    time.sleep(args.delay)

    logging.info("Get xrandr displays")
    screen = get_screen()

    logging.info("Get picture paths")
    picture_paths = get_paths(args.picture_folder)

    thread = threading.Thread(target=loop, daemon=True, args=(screen, picture_paths))
    thread.start()

    show_icon(args, lambda: update_picture(screen, picture_paths, args.brightness), set_spanned)


if __name__ == '__main__':
    main()
