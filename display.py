from PIL import Image, ImageDraw, ImageFont
import sys
import os

# Import official WhisPlay driver
sys.path.append(os.path.expanduser("~/Whisplay/Driver"))
from WhisPlay import WhisPlayBoard  # pyright: ignore[reportMissingImports]


class Display:
    def __init__(self, backlight=60):
        # Initialize hardware
        self.board = WhisPlayBoard()

        # Turn on backlight (important!)
        self.board.set_backlight(backlight)

        # Load a larger readable font
        self.font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            40  # Adjust size if you want bigger/smaller
        )

    def _image_to_rgb565(self, image):
        """Convert PIL image to RGB565 buffer"""
        width, height = image.size
        pixel_data = []

        for y in range(height):
            for x in range(width):
                r, g, b = image.getpixel((x, y))
                rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
                pixel_data.extend([(rgb565 >> 8) & 0xFF, rgb565 & 0xFF])

        return pixel_data

    def update_text(self, text):
        width = self.board.LCD_WIDTH
        height = self.board.LCD_HEIGHT

        # Create blank black image
        image = Image.new("RGB", (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Center the text
        bbox = draw.textbbox((0, 0), text, font=self.font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (width - text_width) // 2
        y = (height - text_height) // 2

        draw.text((x, y), text, font=self.font, fill=(255, 255, 255))

        # Convert to RGB565
        buffer = self._image_to_rgb565(image)

        # Draw to display
        self.board.draw_image(0, 0, width, height, buffer)

    def clear(self):
        self.board.fill_screen(0x0000)  # black

    def cleanup(self):
        self.board.cleanup()