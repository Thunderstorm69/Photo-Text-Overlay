import os
from PIL import Image, ImageDraw, ImageFont

INPUT_FOLDER = "./Input"  
OUTPUT_FOLDER = "./Output"
MAX_TEXT_WIDTH_RATIO = 0.85  # 85% of image width max
SAFE_MARGIN = 30

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def find_scaled_font(text, img_width, font_paths):
    """Find perfect font size that fits image width"""
    target_width = img_width * MAX_TEXT_WIDTH_RATIO
    
    font_size = 12
    best_font = ImageFont.load_default()
    
    while font_size <= 100:  # Max 100px
        test_font = ImageFont.load_default()
        for path in font_paths:
            try:
                test_font = ImageFont.truetype(path, font_size)
                break
            except:
                continue
        
        bbox = ImageDraw.Draw(Image.new('RGB', (1,1))).textbbox((0,0), text, font=test_font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= target_width:
            best_font = test_font
        else:
            break  # Too big, stop
            
        font_size += 2
    
    return best_font, font_size - 2

for filename in os.listdir(INPUT_FOLDER):
    if not (filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff'))):
        continue
    
    img_path = os.path.join(INPUT_FOLDER, filename)
    
    try:
        # Open image
        original = Image.open(img_path)
        width, height = original.size
        
        # Find perfect font size
        text = os.path.splitext(filename)[0]
        font_paths = ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]
        font, font_size = find_scaled_font(text, width, font_paths)
        
        print(f"📏 {filename}: {font_size}px font")
        
        # Create canvas with extra bottom space
        canvas_height = height + 100
        img = Image.new('RGBA', (width, canvas_height), (0,0,0,0))
        img.paste(original, (0, 0))
        
        # Text layer
        text_layer = Image.new('RGBA', img.size, (0,0,0,0))
        draw = ImageDraw.Draw(text_layer)
        
        # **CENTERED POSITION CALCULATION**
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # **CENTER BOTTOM**: x = center of image, y = bottom with margin
        x = (width - text_width) // 2
        y = height
        
        # Thick outline + text
        outline_color = (0, 0, 0, 255)
        text_color = (255, 255, 255, 255)
        
        # Draw thick black outline
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
        
        # Draw white text on top
        draw.text((x, y), text, font=font, fill=text_color)
        
        # Combine layers
        img = Image.alpha_composite(img, text_layer)
        img = img.crop(img.getbbox())
        
        # Save
        out_path = os.path.join(OUTPUT_FOLDER, filename)
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            img.convert('RGB').save(out_path, 'JPEG', quality=95)
        else:
            img.save(out_path, 'PNG')
            
        print(f"✅ {filename} - {font_size}px CENTERED at bottom!")
        
    except Exception as e:
        print(f"❌ Error {filename}: {e}")

print("ALL IMAGES DONE")
