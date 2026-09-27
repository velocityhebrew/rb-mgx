"""
Viral YouTube Thumbnail Generator for Roblox Brainrot AI
Generates high-CTR 1280x720 thumbnails with bold 3D text, neon glow, and meme badges
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

RECORDINGS_DIR = os.path.join(os.path.dirname(__file__), "recordings")


def draw_text_with_outline(draw, pos, text, font, fill_color, stroke_color, stroke_width=6, shadow_offset=(8, 8), shadow_color=(0, 0, 0, 220)):
    x, y = pos
    # Draw drop shadow
    if shadow_offset and shadow_color:
        sx, sy = shadow_offset
        for dx in range(-stroke_width, stroke_width + 1):
            for dy in range(-stroke_width, stroke_width + 1):
                draw.text((x + sx + dx, y + sy + dy), text, font=font, fill=shadow_color)
    
    # Draw stroke
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx * dx + dy * dy <= stroke_width * stroke_width:
                draw.text((x + dx, y + dy), text, font=font, fill=stroke_color)
    
    # Draw main fill
    draw.text((x, y), text, font=font, fill=fill_color)


def generate_thumbnail(
    bg_frame_path=os.path.join(RECORDINGS_DIR, "thumb_frame.jpg"),
    output_path=os.path.join(RECORDINGS_DIR, "thumbnail.png")
):
    print("Generating viral YouTube thumbnail...")
    width, height = 1280, 720
    
    # 1. Base image from gameplay
    if os.path.exists(bg_frame_path):
        base = Image.open(bg_frame_path).convert("RGBA")
        base = base.resize((width, height), Image.Resampling.LANCZOS)
        # Boost color saturation and contrast
        enhancer = ImageEnhance.Color(base)
        base = enhancer.enhance(1.4)
        contrast = ImageEnhance.Contrast(base)
        base = contrast.enhance(1.2)
    else:
        # Fallback neon gradient
        base = Image.new("RGBA", (width, height), (25, 15, 45, 255))
    
    # 2. Add dark vignette around edges to make text pop
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d_overlay = ImageDraw.Draw(overlay)
    
    # Top and bottom subtle gradient bars
    for y in range(160):
        alpha = int(180 * (1.0 - y / 160))
        d_overlay.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
        d_overlay.line([(0, height - 1 - y), (width, height - 1 - y)], fill=(0, 0, 0, alpha))
    
    # Left darkening for text contrast
    for x in range(700):
        alpha = int(140 * (1.0 - x / 700))
        d_overlay.line([(x, 0), (x, height)], fill=(0, 0, 0, alpha))
        
    combined = Image.alpha_composite(base, overlay)
    draw = ImageDraw.Draw(combined)
    
    # Load fonts
    font_path = "C:\\Windows\\Fonts\\impact.ttf"
    if not os.path.exists(font_path):
        font_path = "C:\\Windows\\Fonts\\arialbd.ttf"
        
    f_huge = ImageFont.truetype(font_path, 88)
    f_large = ImageFont.truetype(font_path, 72)
    f_badge = ImageFont.truetype(font_path, 40)
    f_tag = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 26)
    
    # 3. Top Banner Badge ("100-STAGE IMPOSSIBLE OBBY")
    badge_rect = [60, 45, 640, 105]
    draw.rounded_rectangle(badge_rect, radius=12, fill=(255, 0, 60, 230), outline=(255, 255, 255), width=3)
    draw.text((85, 57), "STAGE 100 IMPOSSIBLE OBBY", font=f_badge, fill=(255, 255, 255))
    
    # 4. Main Title Text
    # Line 1: "ONLY 0.1%" in Bright Yellow
    draw_text_with_outline(
        draw, (60, 130), "ONLY 0.1%", f_huge,
        fill_color=(255, 235, 0),
        stroke_color=(0, 0, 0),
        stroke_width=9,
        shadow_offset=(8, 8),
        shadow_color=(180, 0, 0, 240)
    )
    
    # Line 2: "CAN BEAT THIS?!" in Crisp White
    draw_text_with_outline(
        draw, (60, 235), "CAN BEAT THIS?!", f_large,
        fill_color=(255, 255, 255),
        stroke_color=(0, 0, 0),
        stroke_width=8,
        shadow_offset=(7, 7),
        shadow_color=(0, 150, 255, 240)
    )
    
    # 5. Aura Lost Badge (bottom left)
    aura_box = [60, 560, 520, 645]
    draw.rounded_rectangle(aura_box, radius=16, fill=(10, 10, 15, 235), outline=(0, 255, 128), width=4)
    draw.text((80, 580), "AURA: -100,000 [ROASTED]", font=ImageFont.truetype(font_path, 40), fill=(0, 255, 128))
    
    # 6. Eye-catching Right Callout Sticker ("SHAVE EYEBROWS?!")
    callout_box = [820, 120, 1220, 220]
    draw.rounded_rectangle(callout_box, radius=20, fill=(255, 190, 0, 245), outline=(0, 0, 0), width=5)
    draw.text((840, 142), "SHAVE EYEBROWS?!", font=ImageFont.truetype(font_path, 42), fill=(10, 10, 10))
    
    # 7. Red Arrow / Alert Graphic
    arrow_pts = [(1020, 230), (1050, 290), (1000, 280), (980, 370), (940, 360), (960, 270), (910, 280)]
    draw.polygon(arrow_pts, fill=(255, 30, 30), outline=(255, 255, 255))
    
    # 8. Save Thumbnail
    final_rgb = combined.convert("RGB")
    final_rgb.save(output_path, "PNG", quality=95)
    jpg_path = output_path.replace(".png", ".jpg")
    final_rgb.save(jpg_path, "JPEG", quality=92)
    print(f"Viral thumbnail saved: {output_path} & {jpg_path}")
    return output_path


if __name__ == "__main__":
    generate_thumbnail()
