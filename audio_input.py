"""
Handles microphone input and audio recording for Nova.
"""

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

def record_audio(filename: str, duration: int = 5, fs: int = 16000):
	"""
	Records audio from the default microphone and saves as a WAV file.
	Args:
		filename (str): Path to save the recorded audio.
		duration (int): Duration in seconds.
		fs (int): Sample rate.
	"""
	print(f"Recording for {duration} seconds...")
	audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
	sd.wait()
	write(filename, fs, audio)
	print(f"Audio saved to {filename}")
