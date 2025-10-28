"""
Nova: The Ambient Personal AI
Main entry point for the offline AI assistant.
"""

from nova.audio_input import record_audio
from nova.speech_to_text import transcribe_audio
from nova.reasoning_engine import query_ollama
from nova.text_to_speech import synthesize_speech
from nova.memory_manager import save_turn, clear_memory, check_due_reminders
from nova.led_feedback import setup_led, set_led_state

import yaml
import os
import time
from nova.plugins.plugin_manager import NovaPluginManager


def load_tts_config():
    # Try to load user-selected voice from session file
    session_file = "logs/tts_voice.session"
    selected_voice = None
    if os.path.exists(session_file):
        try:
            with open(session_file, "r") as f:
                selected_voice = f.read().strip()
        except Exception:
            selected_voice = None
    try:
        with open("config/config.yaml", "r") as f:
            cfg = yaml.safe_load(f)
        return {
            "voice": selected_voice or cfg.get("coqui_tts_voice", "en_US"),
            "speaker": cfg.get("coqui_tts_speaker", "default"),
            "style": cfg.get("coqui_tts_style", "neutral")
        }
    except Exception as e:
        print("Error loading TTS config:", e)
        return {"voice": selected_voice or "en_US", "speaker": "default", "style": "neutral"}

def main():
    print("Nova: Ambient Personal AI - Starting up...")
    strip = None
    try:
        strip = setup_led()
    except Exception as e:
        print("LED setup error:", e)
    tts_cfg = load_tts_config()
    plugin_manager = NovaPluginManager()
    while True:
        # Sleep/wake cycle: sleep for 10 seconds between interactions (simulated low-power mode)
        print("Nova is idle. Sleeping for 10 seconds...")
        try:
            set_led_state(strip, "idle")
        except Exception as e:
            print("LED idle state error:", e)
        time.sleep(10)
        # Check for due reminders and notify user
        due_reminders = check_due_reminders()
        for r in due_reminders:
            try:
                set_led_state(strip, "speaking")
            except Exception:
                pass
            try:
                synthesize_speech(
                    f"Reminder: {r['routine']}.",
                    tts_endpoint="http://localhost:5002/api/tts",
                    output_path="nova_reminder.wav",
                    voice=tts_cfg["voice"],
                    speaker=tts_cfg["speaker"],
                    style=tts_cfg["style"]
                )
            except Exception as e:
                print("TTS reminder error:", e)
        print("Nova waking up. Ready for interaction.")
        # Listening state
        try:
            set_led_state(strip, "listening")
        except Exception as e:
            print("LED listening state error:", e)
        audio_file = "temp_input.wav"
        try:
            record_audio(audio_file, duration=5)
        except Exception as e:
            print("Audio input error:", e)
            print("Nova could not record audio. Please check your microphone.")
            continue
        # Thinking state
        try:
            set_led_state(strip, "thinking")
        except Exception as e:
            print("LED thinking state error:", e)
        transcript = ""
        try:
            transcript = transcribe_audio(audio_file, whisper_path="./whisper.cpp/main")
            print("Transcript:", transcript)
        except Exception as e:
            print("Speech-to-text error:", e)
            print("Nova could not transcribe audio.")
            continue
        # Run plugins and collect results
        plugin_results = plugin_manager.run_all({"transcript": transcript})
        for pname, presult in plugin_results.items():
            print(f"Plugin [{pname}]: {presult}")
        # Reasoning engine
        if transcript:
            try:
                response = query_ollama(transcript, endpoint="http://localhost:11434/api/generate", model="llama3")
                print("Nova Response:", response)
            except Exception as e:
                print("Reasoning engine error:", e)
                print("Nova could not process your request.")
                continue
            # Combine plugin results with LLM response
            full_response = response
            if plugin_results:
                full_response += "\n" + "\n".join([f"{pname}: {presult}" for pname, presult in plugin_results.items()])
            if response:
                try:
                    set_led_state(strip, "speaking")
                except Exception as e:
                    print("LED speaking state error:", e)
                try:
                    synthesize_speech(
                        full_response,
                        tts_endpoint="http://localhost:5002/api/tts",
                        output_path="nova_reply.wav",
                        voice=tts_cfg["voice"],
                        speaker=tts_cfg["speaker"],
                        style=tts_cfg["style"]
                    )
                except Exception as e:
                    print("TTS error:", e)
                    print("Nova could not speak the response.")
                try:
                    save_turn(transcript, full_response)
                except Exception as e:
                    print("Memory save error:", e)
            else:
                print("No response from reasoning engine.")
        else:
            print("No transcript to process.")

if __name__ == "__main__":
    main()
