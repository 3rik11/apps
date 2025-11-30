from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from time import sleep

# Setup I2C
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

# Font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)

def show(text1, text2=""):
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)

    draw.text((0, 0), text1, font=font, fill=255)
    draw.text((0, 25), text2, font=font, fill=255)

    device.display(image)

def countdown_to_christmas():
    while True:
        now = datetime.now()
        year = now.year

        # If Christmas already passed this year, use next year
        christmas = datetime(year, 12, 25, 0, 0, 0)
        if now > christmas:
            christmas = datetime(year + 1, 12, 25, 0, 0, 0)

        # Difference
        diff = christmas - now

        days = diff.days
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        seconds = diff.seconds % 60

        # Display
        show(
            f"Christmas in:",
            f"{days}d {hours}h {minutes}m {seconds}s"
        )

        sleep(1)

countdown_to_christmas()
