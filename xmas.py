from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from time import sleep
import lgpio

# -------------------------
# OLED setup
# -------------------------
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

# Font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)

# -------------------------
# GPIO setup (safe claim)
# -------------------------
BUTTON_UP = 17

chip = lgpio.gpiochip_open(0)

def safe_claim(pin):
    try:
        lgpio.gpio_claim_input(chip, pin, lgpio.SET_PULL_UP)
    except lgpio.error as e:
        if "busy" in str(e):
            # Pin already claimed by this process → ignore
            pass
        else:
            raise

# Claim the UP button safely
safe_claim(BUTTON_UP)

def button_pressed():
    """Return True if UP button is pressed."""
    return lgpio.gpio_read(chip, BUTTON_UP) == 0

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
        if button_pressed():
            show("Countdown stopped", "")
            break  # Stop the loop if UP button is pressed

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

# -------------------------
# Run countdown
# -------------------------
countdown_to_christmas()

