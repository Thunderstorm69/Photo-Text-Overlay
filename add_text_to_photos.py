import os
from PIL import Image, ImageDraw, ImageFont

INPUT_FOLDER = "."
OUTPUT_FOLDER = "Output"

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp")

BOTTOM_BAR_RATIO = 0.14
MIN_BAR_HEIGHT = 50
MAX_BAR_HEIGHT = 140

TEXT_WIDTH_RATIO = 0.92
START_FONT_RATIO = 0.065
MIN_FONT_SIZE = 12

TEXT_COLOR = (255, 255, 255)
OUTLINE_COLOR = (0, 0, 0)
BAR_COLOR = (0, 0, 0)
JPEG_QUALITY = 97

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\Arialbd.ttf",
    r"C:\Windows\Fonts\segoeuib.ttf",
    r"C:\Windows\Fonts\calibrib.ttf",
]

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def get_font_path():
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


FONT_PATH = get_font_path()


def load_font(size):
    if FONT_PATH:
        return ImageFont.truetype(FONT_PATH, size)
    return ImageFont.load_default()


def fit_font(draw, text, image_width, bar_height):
    max_width = int(image_width * TEXT_WIDTH_RATIO)
    start_size = max(MIN_FONT_SIZE, int(image_width * START_FONT_RATIO))

    for size in range(start_size, MIN_FONT_SIZE - 1, -1):
        font = load_font(size)

        stroke_width = max(2, size // 12)

        bbox = draw.textbbox(
            (0, 0),
            text,
            font=font,
            stroke_width=stroke_width
        )
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if text_width <= max_width and text_height <= int(bar_height * 0.75):
            return font, stroke_width, text_width, text_height, bbox

    font = load_font(MIN_FONT_SIZE)
    stroke_width = max(2, MIN_FONT_SIZE // 12)
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    return font, stroke_width, text_width, text_height, bbox


for filename in os.listdir(INPUT_FOLDER):
    if not filename.lower().endswith(IMAGE_EXTS):
        continue

    input_path = os.path.join(INPUT_FOLDER, filename)

    try:
        original = Image.open(input_path).convert("RGB")
        width, height = original.size

        text = os.path.splitext(filename)[0]

        bar_height = int(height * BOTTOM_BAR_RATIO)
        bar_height = max(MIN_BAR_HEIGHT, min(MAX_BAR_HEIGHT, bar_height))

        canvas = Image.new("RGB", (width, height + bar_height), BAR_COLOR)
        canvas.paste(original, (0, 0))

        draw = ImageDraw.Draw(canvas)

        font, stroke_width, text_width, text_height, bbox = fit_font(
            draw, text, width, bar_height
        )

        text_x = (width - text_width) // 2 - bbox[0]
        text_y = height + (bar_height - text_height) // 2 - bbox[1]

        draw.text(
            (text_x, text_y),
            text,
            font=font,
            fill=TEXT_COLOR,
            stroke_width=stroke_width,
            stroke_fill=OUTLINE_COLOR
        )

        output_path = os.path.join(OUTPUT_FOLDER, filename)

        if filename.lower().endswith((".jpg", ".jpeg")):
            canvas.save(output_path, "JPEG", quality=JPEG_QUALITY, subsampling=0)
        else:
            canvas.save(output_path)

        print(f"Done: {filename}")

    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("All images processed.")
