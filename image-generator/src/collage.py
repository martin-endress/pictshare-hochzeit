from PIL import Image, ImageOps, ImageCms
from pillow_heif import register_heif_opener
import io
import numpy as np



register_heif_opener()

def gamma_correction(img, gamma):
    arr = np.asarray(img).astype("float32") / 255.0
    arr = np.power(arr, gamma)
    arr = np.clip(arr * 255, 0, 255).astype("uint8")
    return Image.fromarray(arr, "RGB")

def open_image_auto(path):
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)

    icc = img.info.get("icc_profile")
    if icc:
        try:
            src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            dst = ImageCms.createProfile("sRGB")
            img = ImageCms.profileToProfile(img, src, dst, outputMode="RGB")
        except Exception:
            img = img.convert("RGB")
    else:
        img = img.convert("RGB")

    if img.mode != "RGB":
        img = img.convert("RGB")

    if img.height > img.width:
        img = img.rotate(90, expand=True)

    return img


def resize_and_crop(img, target_w, target_h):
    target_ratio = 4 / 3
    img_ratio = img.width / img.height

    if img_ratio > target_ratio:
        # Bild ist zu breit
        new_height = target_h
        new_width = int(target_h * img_ratio)
    else:
        # Bild ist zu hoch
        new_width = target_w
        new_height = int(target_w / img_ratio)

    img = img.resize((new_width, new_height), Image.LANCZOS)

    left = (new_width - target_w) // 2
    top = (new_height - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


# Default 10x15 cm @300dpi (Querformat)
def create_collage(
    image_paths,
    output_path="collage_10x15.png",
    gamma=0.85
):
    DPI = 300
    WIDTH = 1772
    HEIGHT = 1181

    CELL_W = 650
    CELL_H = 488

    positions = [
        (51, 51),
        (1071, 51),
        (51, 642),
        (1071, 642),
    ]

    collage = Image.new("RGB", (WIDTH, HEIGHT), "white")

    for path, pos in zip(image_paths, positions):
        img = open_image_auto(path)
        img = resize_and_crop(img, CELL_W, CELL_H)
        img = gamma_correction(img, gamma)
        collage.paste(img, pos)

    collage.save(
        output_path,
        format="PNG",
        dpi=(DPI, DPI)
    )

    return output_path
