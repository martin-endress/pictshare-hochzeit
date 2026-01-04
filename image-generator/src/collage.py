from PIL import Image, ImageOps
from os import path

def normalize_orientation(img):
    img = ImageOps.exif_transpose(img)

    #Flip
    if img.height > img.width:
        img = img.rotate(90, expand=True)

    return img

def resize_and_crop(img, target_w, target_h):
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h

    if img_ratio > target_ratio:
        new_height = target_h
        new_width = int(target_h * img_ratio)
    else:
        new_width = target_w
        new_height = int(target_w / img_ratio)

    img = img.resize((new_width, new_height), Image.LANCZOS)

    left = (new_width - target_w) // 2
    top = (new_height - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


# Default 10x15 cm @300dpi (Querformat)
def create_collage(image_paths, output_path="collage.png", dpi=300, border_px=40, gap_px=20, override_out=False):
    #if len(image_paths) != 4:
    #    raise ValueError("Es braucht 4 Bilder.")

    if not override_out and path.exists(output_path):
        raise ValueError("Error: file " + output_path + " already exists.")


    # pixel dimensions
    WIDTH = int(15 / 2.54 * dpi)
    HEIGHT = int(10 / 2.54 * dpi)

    usable_w = WIDTH - 2 * border_px - gap_px
    usable_h = HEIGHT - 2 * border_px - gap_px

    cell_w = usable_w // 2
    cell_h = usable_h // 2

    collage = Image.new("RGB", (WIDTH, HEIGHT), "white")

    positions = [
        (border_px, border_px),
        (border_px + cell_w + gap_px, border_px),
        (border_px, border_px + cell_h + gap_px),
        (border_px + cell_w + gap_px, border_px + cell_h + gap_px),
    ]

    for img_path, pos in zip(image_paths, positions):
        img = Image.open(img_path)
        img = normalize_orientation(img)
        img = img.convert("RGB")
        img = resize_and_crop(img, cell_w, cell_h)
        collage.paste(img, pos)

    collage.save(
        output_path,
        format="PNG",
        dpi=(dpi, dpi)
    )

    return output_path
