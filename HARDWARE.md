# Nova Hardware Setup Guide

## LED Ring (WS2812)
- **Component:** WS2812 12-LED ring
- **Pinout:**
  - Data In: GPIO 18 (default)
  - Power: 5V
  - Ground: GND
- **Wiring Diagram:**

```
Raspberry Pi GPIO
+-------------------+
| 5V   --- LED VCC  |
| GND  --- LED GND  |
| GPIO18 --- LED DIN|
+-------------------+
```

- **Tips:**
  - Use a level shifter for Data In if needed (Pi GPIO is 3.3V, WS2812 expects 5V).
  - Keep wires short to reduce signal loss.

## Microphone
- **Component:** USB or 3.5mm analog mic
- **Connection:** Plug into Pi/PC USB or audio jack
- **Config:**
  - Test with `arecord -l` (Linux)
  - Set device in `config.yaml` if needed

## Speaker
- **Component:** USB or 3.5mm analog speaker
- **Connection:** Plug into Pi/PC USB or audio jack
- **Config:**
  - Test with `aplay -l` (Linux)
  - Set device in `config.yaml` if needed

## Power
- **Raspberry Pi:**
  - Use official 5V/3A power supply
  - Ensure enough current for LED ring

## References
- [rpi_ws281x](https://github.com/jgarff/rpi_ws281x)
- [Raspberry Pi GPIO Pinout](https://pinout.xyz/)

---
*For questions or troubleshooting, see README or open an issue.*
