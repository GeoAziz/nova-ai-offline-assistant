"""
Nova: The Ambient Personal AI
Main entry point for the offline AI assistant.
"""

from audio_input import record_audio
from speech_to_text import transcribe_audio

from reasoning_engine import query_ollama


from text_to_speech import synthesize_speech
from memory_manager import save_turn, clear_memory
from led_feedback import setup_led, set_led_state

def main():
    print("Nova: Ambient Personal AI - Starting up...")
    strip = setup_led()
    # Listening state
    set_led_state(strip, "listening")
    audio_file = "temp_input.wav"
    record_audio(audio_file, duration=5)
    # Thinking state
    set_led_state(strip, "thinking")
    transcript = transcribe_audio(audio_file, whisper_path="./whisper.cpp/main")
    print("Transcript:", transcript)
    # Reasoning engine
    if transcript:
        response = query_ollama(transcript, endpoint="http://localhost:11434/api/generate", model="llama3")
        print("Nova Response:", response)
        if response:
            set_led_state(strip, "speaking")
            synthesize_speech(response, tts_endpoint="http://localhost:5002/api/tts", output_path="nova_reply.wav")
            save_turn(transcript, response)
        else:
            print("No response from reasoning engine.")
    else:
        print("No transcript to process.")
    # Idle state
    set_led_state(strip, "idle")

if __name__ == "__main__":
    main()
