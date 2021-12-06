import os
import tempfile
import logging

import cv2

from fakexrandr_background.picture_utils import create_picture


def set_spanned():
    logging.info("Set gsettings set org.gnome.desktop.background picture-options to spanned")
    os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-options 'spanned'")


def update_picture(screen, picture_paths, brightness):
    logging.info("Generating picture...")
    background = create_picture(screen, picture_paths, brightness)

    with tempfile.NamedTemporaryFile() as tmp:
        cv2.imwrite(tmp.name + ".jpg", background)
        logging.info("Picture saved")

        os.system(f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri file:///{tmp.name}.jpg")
        logging.info("Background updated")
