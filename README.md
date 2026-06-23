# Photo Text Overlay with Python

A simple Python script that adds each image's filename as text at the bottom of the photo.

It is designed for **Windows + Pillow** and was built for batch-processing folders of old photos where every image already has a useful filename.

## What it does

- Reads all images from a folder.
- Uses the filename (without `.jpg`, `.png`, etc.) as the text label.
- Scales the font size based on the image width.
- Centers the text at the bottom.
- Draws a black box behind the text for readability.
- Saves the edited images into an `output` folder.

## Features

- Batch processes multiple images.
- Works with `.jpg`, `.jpeg`, `.png`, `.bmp`, and `.tiff` files.
- Automatically adjusts text size for short and long filenames.
- Adds bold white text with a thick black outline.
- Keeps the original image untouched by saving results separately.

## Requirements

- Python 3
- Pillow

Install Pillow with:

```bash
python -m pip install pillow
```

If `pip` is not recognized on Windows, try:

```bash
py -m pip install pillow
```

## How to use

1. Put the script in the same folder as your photos.
2. Save it as `add_text_to_photos.py`.
3. Open Command Prompt or PowerShell in that folder.
4. Run:

```bash
python add_text_to_photos.py
```

5. Check the `output` folder for the edited images.

## Folder structure

```text
project-folder/
├── add_text_to_photos.py
├── photo1.jpg
├── photo2.jpg
├── photo3.png
└── output/
```

## Notes

- The script uses Windows font paths by default.
- If Arial is not available, Pillow will fall back to its default font.
- Very long filenames are automatically reduced in size to fit the image width.
- The original files are not overwritten.

## Example use cases

- Labeling scanned photo archives.
- Adding captions based on file names.
- Organizing old album images before sharing.
- Preparing images for family, school, or project archives.

## License

You can add your preferred license here, for example MIT.
