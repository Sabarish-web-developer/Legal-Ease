import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs(r"c:\Legalease\Image", exist_ok=True)

def draw_balance_scale(draw, x_center, y_center, scale=1.0, color=(255, 255, 255)):
    # Base
    base_w = 40 * scale
    base_h = 6 * scale
    draw.rectangle([x_center - base_w/2, y_center + 26 * scale, x_center + base_w/2, y_center + 26 * scale + base_h], fill=color)
    
    # Pillar
    pillar_w = 6 * scale
    draw.rectangle([x_center - pillar_w/2, y_center - 24 * scale, x_center + pillar_w/2, y_center + 26 * scale], fill=color)
    
    # Top finial / circle
    finial_r = 6 * scale
    draw.ellipse([x_center - finial_r, y_center - 30 * scale - finial_r, x_center + finial_r, y_center - 30 * scale + finial_r], fill=color)
    
    # Crossbeam
    beam_w = 70 * scale
    draw.line([x_center - beam_w/2, y_center - 20 * scale, x_center + beam_w/2, y_center - 20 * scale], fill=color, width=int(4 * scale))
    
    # Left Pan
    left_x = x_center - beam_w/2
    draw.line([left_x, y_center - 20 * scale, left_x - 14 * scale, y_center + 6 * scale], fill=color, width=int(2 * scale))
    draw.line([left_x, y_center - 20 * scale, left_x + 14 * scale, y_center + 6 * scale], fill=color, width=int(2 * scale))
    draw.arc([left_x - 16 * scale, y_center - 4 * scale, left_x + 16 * scale, y_center + 12 * scale], 0, 180, fill=color, width=int(3 * scale))
    draw.line([left_x - 16 * scale, y_center + 4 * scale, left_x + 16 * scale, y_center + 4 * scale], fill=color, width=int(2 * scale))

    # Right Pan
    right_x = x_center + beam_w/2
    draw.line([right_x, y_center - 20 * scale, right_x - 14 * scale, y_center + 6 * scale], fill=color, width=int(2 * scale))
    draw.line([right_x, y_center - 20 * scale, right_x + 14 * scale, y_center + 6 * scale], fill=color, width=int(2 * scale))
    draw.arc([right_x - 16 * scale, y_center - 4 * scale, right_x + 16 * scale, y_center + 12 * scale], 0, 180, fill=color, width=int(3 * scale))
    draw.line([right_x - 16 * scale, y_center + 4 * scale, right_x + 16 * scale, y_center + 4 * scale], fill=color, width=int(2 * scale))

def generate_logo(filename, is_dark_bg=False):
    width, height = 400, 120
    bg_color = (15, 23, 42, 255) if is_dark_bg else (255, 255, 255, 0)
    fg_color = (255, 255, 255) if is_dark_bg else (30, 41, 59)
    
    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw icon on the left
    draw_balance_scale(draw, 65, 60, scale=1.1, color=fg_color)
    
    # Try loading a system font or default font
    try:
        font = ImageFont.truetype("arial.ttf", 44)
    except Exception:
        font = ImageFont.load_default()
        
    draw.text((130, 36), "LegalEase", fill=fg_color, font=font)
    img.save(filename)
    print(f"Saved {filename}")

generate_logo(r"c:\Legalease\Image\Logo.png", is_dark_bg=False)
generate_logo(r"c:\Legalease\Image\inverseLogo.png", is_dark_bg=True)
