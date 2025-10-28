def get_available_voices(tts_endpoint: str = "http://localhost:5002/api/voices"):
	"""
	Fetch available voices from Coqui TTS server.
	Returns a list of voice dicts (name, language, style).
	"""
	try:
		response = requests.get(tts_endpoint)
		response.raise_for_status()
		return response.json().get("voices", [])
	except Exception as e:
		print("Error fetching TTS voices:", e)
		return []
"""
Integrates Coqui TTS for offline text-to-speech synthesis.
"""

import requests
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile

def synthesize_speech(text: str, tts_endpoint: str = "http://localhost:5002/api/tts", output_path: str = "nova_reply.wav", voice: str = "en_US", speaker: str = "default", style: str = "neutral"):
	"""
	Synthesizes speech using Coqui TTS server and plays the audio.
	Args:
		text (str): Text to synthesize.
		tts_endpoint (str): Coqui TTS API endpoint.
		output_path (str): Path to save the generated audio.
		voice (str): Language/accent code (e.g., 'en_US').
		speaker (str): Speaker voice name.
		style (str): Speaking style (e.g., 'neutral', 'happy').
	"""
	payload = {
		"text": text,
		"voice": voice,
		"speaker": speaker,
		"style": style
	}
	try:
		response = requests.post(tts_endpoint, json=payload)
		response.raise_for_status()
		with open(output_path, "wb") as f:
			f.write(response.content)
		print(f"Synthesized speech saved to {output_path}")
		# Play audio
		fs, audio = wavfile.read(output_path)
		sd.play(audio, fs)
		sd.wait()
	except Exception as e:
		print("Coqui TTS error:", e)
