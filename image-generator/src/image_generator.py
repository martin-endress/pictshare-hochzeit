from collage import create_collage
from pathlib import Path
from datetime import datetime
from time import sleep
from glob import glob
import subprocess
import os

IMAGES_DIR = Path("images")
COLLAGES_DIR = IMAGES_DIR / "collages"
ARCHIVE_DIR = IMAGES_DIR / "archive"

def init_folders():
    COLLAGES_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

def process_images(images):
    out_path = COLLAGES_DIR / 'collage_{date:%Y-%m-%d_%H-%M-%S}.png'.format(date=datetime.now())
    create_collage(images, output_path=out_path)
    # mv to archive
    for image in images:
        os.rename(image, ARCHIVE_DIR / image.name)
    # print
    lp =  subprocess.run(["lp", str(out_path)])


def main():
    print("Starting image generation...")
    
    init_folders()

    glob_regex = "images/*.png/*.png"

    while True:
        image_queue = [Path(x) for x in glob(glob_regex)]
        # idk if this is necessary
        sleep(1)
        if len(image_queue) == 0:
            print("Queue empty, waiting...")
        elif len(image_queue) < 4:
            print("Queue contains {l} entries, waiting...".format(l=len(image_queue)))
        else:
            print("Queue contains {l} entries. Processing 4 images...".format(l=len(image_queue)))
            process_images(image_queue[:4])
        sleep(5)

if __name__ == '__main__':
    main()
