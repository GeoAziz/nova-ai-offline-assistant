"""
Controls LED ring or RGB light for Nova's state feedback.
"""

import time
try:
	from rpi_ws281x import PixelStrip, Color
except ImportError:
	PixelStrip = None
	Color = None

# LED configuration
LED_COUNT = 12      # Number of LED pixels
LED_PIN = 18        # GPIO pin (default)
LED_BRIGHTNESS = 64 # Brightness (0-255)

def setup_led():
	if PixelStrip is None:
		print("rpi_ws281x not available. LED feedback disabled.")
		return None
	strip = PixelStrip(LED_COUNT, LED_PIN, brightness=LED_BRIGHTNESS)
	strip.begin()
	return strip

def set_led_state(strip, state: str):
	"""
	Set LED color/effect based on Nova state.
	States: listening, thinking, speaking, idle
	Advanced: breathing, rainbow, pulse animations.
	"""
	if strip is None:
		return
	color_map = {
		"listening": Color(0, 0, 255),    # Soft blue
		"thinking": Color(255, 255, 255), # White pulse
		"speaking": Color(255, 140, 0),   # Warm amber
		"idle": Color(0, 0, 0)            # Off
	}
	color = color_map.get(state, Color(0, 0, 0))
	for i in range(LED_COUNT):
		strip.setPixelColor(i, color)
	strip.show()
	if state == "thinking":
		# Pulse effect
		for b in range(20, LED_BRIGHTNESS, 5):
			strip.setBrightness(b)
			strip.show()
			time.sleep(0.03)
		for b in range(LED_BRIGHTNESS, 20, -5):
			strip.setBrightness(b)
			strip.show()
			time.sleep(0.03)
	if state == "listening":
		# Breathing animation stub
		for b in range(20, LED_BRIGHTNESS, 8):
			strip.setBrightness(b)
			strip.show()
			time.sleep(0.05)
		for b in range(LED_BRIGHTNESS, 20, -8):
			strip.setBrightness(b)
			strip.show()
			time.sleep(0.05)
	if state == "speaking":
		# Rainbow animation stub
		for j in range(LED_COUNT):
			strip.setPixelColor(j, Color((j*20)%255, (255-j*20)%255, (j*10)%255))
		strip.show()
		time.sleep(0.2)
