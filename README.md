# Nova: The Ambient Personal AI

## Mission
Build a privacy-first, offline, human-like AI assistant that listens, thinks, and speaks — all locally, with zero cloud dependencies.

## Quickstart
1. Clone repo
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `.env` or `config.yaml` for model paths and hardware
4. [Set up hardware](HARDWARE.md) (LED ring, mic, speaker)
5. Build and run all services:
   ```zsh
   docker-compose up --build
   ```
6. Access Nova’s web interface at [http://localhost:5000](http://localhost:5000)

## Architecture
- **Audio Input:** `audio_input.py` — records mic input
- **Speech-to-Text:** `speech_to_text.py` — Whisper.cpp integration
- **Reasoning:** `reasoning_engine.py` — Ollama LLM
- **Text-to-Speech:** `text_to_speech.py` — Coqui TTS
- **LED Feedback:** `led_feedback.py` — ambient hardware states
- **Memory:** `memory_manager.py` — local conversation history
- **Interface:** `interface.py` — Flask web dashboard

## Testing
Run unit tests for each module:
```zsh
python -m unittest test_led_feedback.py
python -m unittest test_interface.py
```

## Ethical Manifesto
- 100% local data processing
- No telemetry, tracking, or ads
- Simple privacy controls

## Hardware Setup
See [HARDWARE.md](HARDWARE.md) for wiring diagrams and tips.

## Troubleshooting
- Check Docker logs for errors
- Ensure hardware is wired and powered correctly
- For LED issues, verify `rpi_ws281x` installation and GPIO pin

## References
- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp)
- [Ollama](https://ollama.com)
- [Coqui TTS](https://github.com/coqui-ai/TTS)
- [rpi_ws281x](https://github.com/jgarff/rpi_ws281x)

---
*Technology that disappears until it helps you.*
