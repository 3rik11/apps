from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from time import sleep
import os
import lgpio

# -------------------------
# OLED setup
# -------------------------
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

# Font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)

# -------------------------
# lgpio button setup
# -------------------------
BUTTON_UP = 17
BUTTON_DOWN = 27
BUTTON_SELECT = 22

chip = lgpio.gpiochip_open(0)

# claim pins as inputs with pull-ups
lgpio.gpio_claim_input(chip, BUTTON_UP, lgpio.SET_PULL_UP)
lgpio.gpio_claim_input(chip, BUTTON_DOWN, lgpio.SET_PULL_UP)
lgpio.gpio_claim_input(chip, BUTTON_SELECT, lgpio.SET_PULL_UP)

def get_button():
    if lgpio.gpio_read(chip, BUTTON_UP) == 0:
        return "UP"
    if lgpio.gpio_read(chip, BUTTON_DOWN) == 0:
        return "DOWN"
    if lgpio.gpio_read(chip, BUTTON_SELECT) == 0:
        return "SELECT"
    return None

def check_reboot_button():
    """Reboot Pi if SELECT is pressed."""
    if lgpio.gpio_read(chip, BUTTON_SELECT) == 0:
        show("Rebooting...", "")
        sleep(1)
        os.system("sudo reboot now")

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
        check_reboot_button()

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
