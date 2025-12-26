import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Configuration
# Run from scripts/ directory or adjust paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SOURCE_DIR = os.path.join(PROJECT_ROOT, "importantexperimentlogs")
DEST_DIR = os.path.join(PROJECT_ROOT, "importantexperimentphotos")

FONT_SIZE = 14
PADDING = 20
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
YAML_BG_COLOR = (40, 44, 52)
LOG_BG_COLOR = (20, 20, 20)

def ensure_dir_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def create_image(yaml_path, log_path, output_path):
    yaml_content = read_file(yaml_path)
    log_content = read_file(log_path)
    
    # Try to load a monospace font
    try:
        # Standard locations
        font_paths = [
            "DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/System/Library/Fonts/Monaco.ttf" 
        ]
        font = None
        for path in font_paths:
            try:
                font = ImageFont.truetype(path, FONT_SIZE)
                break
            except IOError:
                continue
        
        if font is None:
             font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    # Calculate dimensions
    # helper to measure text
    def measure_text(text, font):
        lines = text.split('\n')
        max_w = 0
        total_h = 0
        for line in lines:
            if hasattr(font, 'getbbox'):
                bbox = font.getbbox(line)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1] + 4 # line height + padding
            else:
                 # Fallback for default font which might not support getbbox well in older Pillow
                 w = len(line) * 7
                 h = 15
            
            if w > max_w: max_w = w
            total_h += h
        return max(max_w, 400), total_h + PADDING

    yaml_w, yaml_h = measure_text(yaml_content, font)
    log_w, log_h = measure_text(log_content, font)
    
    # Fixed widths for layout
    col_width = max(800, max(yaml_w, log_w) + PADDING * 2) # Slightly wider for single column
    
    total_width = col_width + PADDING * 2
    total_height = yaml_h + log_h + PADDING * 6 + 100 # ample vertical space
    
    # Create image
    img = Image.new('RGB', (total_width, total_height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Draw backgrounds
    # Top section for YAML
    draw.rectangle([0, 0, total_width, yaml_h + PADDING * 3 + 50], fill=YAML_BG_COLOR)
    # Bottom section for Log
    draw.rectangle([0, yaml_h + PADDING * 3 + 50, total_width, total_height], fill=LOG_BG_COLOR)
    
    # Draw Headers
    header_y_yaml = PADDING
    header_y_log = yaml_h + PADDING * 4 + 50
    
    draw.text((PADDING, header_y_yaml), f"YAML Config: {os.path.basename(yaml_path)}", font=font, fill=(0, 255, 200))
    draw.text((PADDING, header_y_log), f"Log Output: {os.path.basename(log_path)}", font=font, fill=(0, 255, 0))
    
    # Draw Content
    def draw_text_content(text, x, y, font, color):
        lines = text.split('\n')
        curr_y = y
        line_height = 15
        if hasattr(font, 'getbbox'):
             line_height = font.getbbox("A")[3] + 4
             
        for line in lines:
            draw.text((x, curr_y), line, font=font, fill=color)
            curr_y += line_height

    content_y_yaml = header_y_yaml + 40
    content_y_log = header_y_log + 40

    draw_text_content(yaml_content, PADDING, content_y_yaml, font, TEXT_COLOR)
    draw_text_content(log_content, PADDING, content_y_log, font, TEXT_COLOR)
    
    ensure_dir_exists(os.path.dirname(output_path))
    img.save(output_path)
    print(f"Generated: {output_path}")

def main():
    if not os.path.exists(SOURCE_DIR):
        print(f"Source directory not found: {SOURCE_DIR}")
        return

    ensure_dir_exists(DEST_DIR)
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".log"):
                base_name = os.path.splitext(file)[0]
                # Look for matching yaml
                yaml_file = base_name + ".yaml"
                
                if yaml_file in files:
                    log_path = os.path.join(root, file)
                    yaml_path = os.path.join(root, yaml_file)
                    
                    # Calculate relative path to maintain structure
                    rel_path = os.path.relpath(root, SOURCE_DIR)
                    if rel_path == ".":
                        output_dir = DEST_DIR
                    else:
                        output_dir = os.path.join(DEST_DIR, rel_path)
                    
                    output_filename = f"{base_name}.png"
                    output_path = os.path.join(output_dir, output_filename)
                    create_image(yaml_path, log_path, output_path)

if __name__ == "__main__":
    main()
