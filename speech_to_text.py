"""
Integrates Whisper.cpp for offline speech-to-text transcription.
"""

import subprocess

def transcribe_audio(audio_path: str, whisper_path: str = "./whisper.cpp/main") -> str:
	"""
	Transcribes audio using Whisper.cpp executable.
	Args:
		audio_path (str): Path to .wav file.
		whisper_path (str): Path to Whisper.cpp executable.
	Returns:
		str: Transcribed text.
	"""
	print(f"Transcribing {audio_path} with Whisper.cpp...")
	result = subprocess.run([
		whisper_path,
		"-f", audio_path,
		"-m", "models/ggml-base.en.bin",
		"-otxt"
	], capture_output=True, text=True)
	if result.returncode != 0:
		print("Whisper.cpp error:", result.stderr)
		return ""
	# Read output from generated .txt file
	txt_path = audio_path.replace('.wav', '.txt')
	try:
		with open(txt_path, 'r') as f:
			transcript = f.read().strip()
		print("Transcription complete.")
		return transcript
	except Exception as e:
		print("Error reading transcript:", e)
		return ""
