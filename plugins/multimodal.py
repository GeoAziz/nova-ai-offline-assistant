"""
Example Multi-modal Input Plugin for Nova (image/sensor)
"""
from PIL import Image
import os

def run(context):
    image_path = context.get("image_path")
    if image_path and os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            info = f"Image size: {img.size}, mode: {img.mode}"
            return f"Processed image: {info}"
        except Exception as e:
            return f"Image processing error: {e}"
    else:
        return "No image provided or file not found."
