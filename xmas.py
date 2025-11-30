from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from time import sleep
import RPi.GPIO as GPIO
import os

# -------------------------
# OLED setup
# -------------------------
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

# Font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)

# -------------------------
# GPIO setup for buttons
# -------------------------
BUTTON_UP = 17
BUTTON_DOWN = 27
BUTTON_SELECT = 22  # reboot trigger

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_SELECT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# -------------------------
# Helper: wait for select press
# -------------------------
def check_reboot_button():
    """If SELECT is pressed, reboot the Pi."""
    if GPIO.input(BUTTON_SELECT) == GPIO.LOW:
        os.system("sudo reboot")
        while True:
            pass  # prevent continuing code

# -------------------------
# Display helper
# -------------------------
def show(text1, text2=""):
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text1, font=font, fill=255)
    draw.text((0, 25), text2, font=font, fill=255)
    device.display(image)

# -------------------------
# Christmas Countdown Loop
# -------------------------
def countdown_to_christmas():
    while True:
        check_reboot_button()  # check every loop

        now = datetime.now()
        year = now.year

        # Determine correct Christmas date
        christmas = datetime(year, 12, 25)
        if now > christmas:
            christmas = datetime(year + 1, 12, 25)

        # Time remaining
        diff = christmas - now

        days = diff.days
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        seconds = diff.seconds % 60

        # Display
        show(
            "Christmas in:",
            f"{days}d {hours}h {minutes}m {seconds}s"
        )

        sleep(1)

countdown_to_christmas()
