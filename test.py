from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont, ImageOps
from time import sleep
from random import randint
import os

# Setup I2C
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)
    
# -------------------------
# Variables: Fonts
# -------------------------
norm = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
italic = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"


# -------------------------
# Function: Clear display
# -------------------------
def clear_screen():
    device.clear()

# -------------------------
# Function: Display text
# -------------------------
def show_text(text, font_path=norm, size=16, invert=False, center=False):
    
    # Create blank image
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)
    
    # Load font
    font = ImageFont.truetype(font_path, size)
    
    # Calculate position
    if center:
        bbox = draw.textbbox((0, 0), text, font=font)  # returns (x0, y0, x1, y1)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (device.width - text_width) // 2
        y = (device.height - text_height) // 2
    else:
        x, y = 0, 0
    
    # Draw text
    draw.text((x, y), text, font=font, fill=255)
    
    # Invert if needed
    if invert:
        image = ImageOps.invert(image)
    
    # Display
    device.display(image)


# -------------------------
# Function: Display image
# -------------------------
def show_image(image_path, invert=False):
    image = Image.open(image_path).convert("1").resize((device.width, device.height))
    if invert:
        image = ImageOps.invert(image)
    device.display(image)

# -------------------------
# Function: Invert display
# -------------------------
def invert_display(on=True):
    device.invert(on)

def has_files(folder_path):
    """
    Returns True if the folder contains one or more files,
    False if it contains no files or does not exist.
    """
    if not os.path.exists(folder_path):
        return False  # Folder doesn't exist

    # Count the number of files in the folder
    file_count = sum(1 for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))
    
    return file_count > 0


show_text("test app works :)")
