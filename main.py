from display import Display
import time

display = Display(backlight=70)
display.update_text("HELLO")

time.sleep(10)
display.cleanup()

