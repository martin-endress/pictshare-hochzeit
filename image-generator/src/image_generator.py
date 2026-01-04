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

WAIT_THRESHOLD = int(os.getenv("IMAGE_WAIT_THRESHOLD", "60"))
GAMMA_CORRECT = float(os.getenv("GAMMA_CORRECT", "0.85"))

def init_folders():
    COLLAGES_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

def process_images(images):
    out_path = COLLAGES_DIR / 'collage_{date:%Y-%m-%d_%H-%M-%S}.png'.format(date=datetime.now())
    create_collage(images, output_path=out_path, gamma=GAMMA_CORRECT)
    # mv to archive
    for image in images:
        image.rename(ARCHIVE_DIR / image.name)
        #os.rename(image, ARCHIVE_DIR / image.name)
    # print
    lp =  subprocess.run(["lp", str(out_path)])


def main():
    print("Starting image generation.")
    print("\tthreshold: {threshold} seconds\n\tgamma correction: {gamma:.3f}.".format(threshold=WAIT_THRESHOLD, gamma=GAMMA_CORRECT))
    
    init_folders()

    glob_regex = "images/*/*.*"
    excluded_folders = ['archive', 'collages']

    contains_items = False
    started_waiting = int(datetime.now().timestamp())

    while True:
        image_queue = [Path(x) for x in glob(glob_regex) if Path(x).parent.name not in excluded_folders]
        # idk if this is necessary
        sleep(1)
        if len(image_queue) == 0:
            contains_items = False
            print("Queue empty, waiting for images.")
        elif len(image_queue) < 4:
            if not contains_items:
                contains_items = True
                started_waiting = int(datetime.now().timestamp())
            waiting_for_seconds = int(datetime.now().timestamp()) - started_waiting
            if waiting_for_seconds >= WAIT_THRESHOLD:
                print("Queue contains {l} entries. Processing images after wait threshold is reached (wait={wait})".format(l=len(image_queue), wait=waiting_for_seconds))
                selected_images = image_queue
                process_images(selected_images)
                contains_items = False
            else:
                print("Queue contains {l} entries. Have been waiting for {wait} seconds now.".format(l=len(image_queue), wait=waiting_for_seconds))
        else:
            print("Queue contains {l} entries. Processing 4 images...".format(l=len(image_queue)))
            selected_images = image_queue[:4]
            process_images(selected_images)
            contains_items = False
        sleep(4)

if __name__ == '__main__':
    main()
