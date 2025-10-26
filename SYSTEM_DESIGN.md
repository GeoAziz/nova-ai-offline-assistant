# ⚙️ SYSTEM ANALYSIS AND DESIGN

## Project: Nova — The Ambient Personal AI

### 1. System Overview
Nova is an intelligent voice-based assistant designed to function entirely offline, providing personalized interactions while maintaining full user privacy. The system captures audio input, processes it locally using machine learning models, generates context-aware responses, and delivers them as synthesized speech.

It represents a closed-loop AI system consisting of four core modules:
- Input Processing (Voice Capture & Speech Recognition)
- Reasoning Engine (Natural Language Understanding)
- Output Generation (Text-to-Speech)
- User Interface & Feedback (Visual and Log-based)

### 2. System Analysis
#### a. Functional Requirements
| Functionality           | Description                                      |
|------------------------|--------------------------------------------------|
| Voice input capture    | Records audio from the user through a microphone. |
| Speech recognition     | Converts spoken input into text locally.          |
| Natural language reasoning | Processes the transcribed text using an LLM for intent and response. |
| Speech synthesis       | Converts textual responses into audio output.     |
| Offline operation      | All modules execute on the local device, no internet required. |
| Logging                | Stores interaction history locally for transparency. |
| Privacy management     | Provides clear data deletion and user control.    |
| Visual feedback        | Indicates Nova’s current state (Listening / Thinking / Speaking). |

#### b. Non-Functional Requirements
| Category        | Specification                                        |
|----------------|------------------------------------------------------|
| Performance    | Response time < 3 seconds for standard queries.      |
| Scalability    | System can run on Raspberry Pi 5 or laptop.          |
| Usability      | Simple, minimalist design; intuitive interaction.    |
| Reliability    | Must handle multiple queries without system crash.   |
| Security & Privacy | No cloud or external API calls.                  |
| Portability    | Works across Linux, macOS, or embedded systems.      |
| Maintainability| Modular Python codebase; easily upgradable models.   |

### 3. System Architecture Design
#### a. Architecture Type: Modular Layered Architecture
Nova uses a layered modular structure to isolate concerns and make future enhancements easy.

#### b. System Architecture Diagram
```
+---------------------------------------------------+
|                 User Interface Layer              |
|  (Microphone, Speaker, LED Ring, Dashboard)       |
+---------------------------------------------------+
|            Application Control Layer              |
|  (Python Controller: nova.py)                     |
+---------------------------------------------------+
|        Processing & Intelligence Layer            |
|   - Whisper.cpp (Speech-to-Text)                  |
|   - Ollama + Llama3 (Reasoning Engine)            |
|   - Coqui TTS (Speech Synthesis)                  |
+---------------------------------------------------+
|                Hardware / OS Layer                |
|   - Audio Drivers, GPIO, Storage, CPU             |
+---------------------------------------------------+
```
Each layer communicates via clean interfaces, ensuring modularity and easy debugging.

#### c. Data Flow Diagram (DFD)
**Level 0 – Context Diagram**
```
┌──────────────┐
│   User       │
│ (Speaks)     │
└──────┬───────┘
       │ Voice Input
       ▼
┌──────────────┐
│   Nova AI    │
│ (Offline System) │
└──────┬───────┘
       │ Spoken Response
       ▼
┌──────────────┐
│   User       │
│ (Listens)    │
└──────────────┘
```
**Level 1 – Detailed DFD**
```
        +-------------------+
        |   Microphone      |
        +---------+---------+
                  |
                  | Audio Data
                  v
       +------------------------+
       | Speech Recognition     |
       | (Whisper.cpp)          |
       +---------+--------------+
                 |
                 | Transcribed Text
                 v
       +------------------------+
       | Reasoning Engine       |
       | (Ollama + Llama3)      |
       +---------+--------------+
                 |
                 | Text Response
                 v
       +------------------------+
       | Speech Synthesis       |
       | (Coqui TTS)            |
       +---------+--------------+
                 |
                 | Voice Output
                 v
             +---+---+
             | Speaker|
             +--------+
```
#### d. Use Case Diagram
```
        +-----------+
        |   User    |
        +-----+-----+
              |
              | Speaks Commands / Listens
              v
        +--------------------+
        |     Nova System    |
        +--------------------+
              ^          ^
              |          |
   +----------+   +------+---------+
   |                      |
View Logs          Manage Settings
(Delete History)   (Adjust Voice)
```

### 4. Detailed Module Description
#### 🧩 Module 1: Voice Input & Speech Recognition
- Tool: Whisper.cpp
- Input: Audio from microphone (WAV format)
- Output: Transcribed text
- Process:
  - Record 5–10 seconds of audio
  - Convert to text using a local model (base.en)
  - Pass text to reasoning module

#### 🧩 Module 2: Reasoning Engine
- Tool: Ollama with Llama 3 or Mistral model
- Input: Transcribed user text
- Output: Natural language response
- Process:
  - Receive prompt from user
  - Generate response using local LLM
  - Return structured reply to speech module

#### 🧩 Module 3: Text-to-Speech (TTS)
- Tool: Coqui TTS
- Input: Text output from reasoning module
- Output: Spoken response (audio)
- Features:
  - Natural English accent
  - Adjustable pitch and speed
  - Saves output as temporary WAV and plays

#### 🧩 Module 4: User Interface Layer
- Implementation Options:
  - CLI (Console-based)
  - Flask Web Dashboard (visual states)
  - LED Ring for ambient feedback
- System States:
  | State     | Indicator         |
  |-----------|------------------|
  | Listening | LED soft blue glow|
  | Thinking  | LED pulsing amber |
  | Speaking  | LED white glow    |
  | Idle      | LED off           |

### 5. Database / Data Design
No external database used — everything is file-based and local.

**Log file structure (nova.log):**
| Field        | Description                |
|--------------|---------------------------|
| Timestamp    | Date & time of query       |
| User Input   | Transcribed text           |
| Response     | Model-generated reply      |
| Duration     | Processing time            |

Example:
`[2025-10-26 15:32] User: "What's the time?" → Nova: "It’s 3:32 PM."`

### 6. System Design Features
| Feature      | Description                |
|--------------|---------------------------|
| Modularity   | Each function (STT, LLM, TTS) is isolated and replaceable. |
| Offline Operation | All models and processes run locally. |
| Transparency | Logs available to user anytime. |
| Minimalism   | No GUI overload — focus on natural interaction. |
| Scalability  | Models can be swapped for lighter or larger versions. |

### 7. System Testing
| Test Case                | Expected Output           | Result   |
|--------------------------|--------------------------|----------|
| Speech recognition (clear voice) | Accurate transcription | ✅ Pass |
| Background noise test    | Minor recognition loss    | ⚠ Partial|
| LLM reasoning            | Relevant, contextual reply| ✅ Pass |
| TTS output               | Smooth, human-like speech | ✅ Pass |
| Offline operation        | No network access needed  | ✅ Pass |
| Privacy deletion         | Log file erased           | ✅ Pass |

### 8. Security and Privacy Measures
| Concern         | Mitigation                       |
|-----------------|----------------------------------|
| Data leakage    | No network connectivity during use.|
| Voice misuse    | Audio deleted after transcription.|
| Transparency    | Interaction logs stored locally.  |
| User control    | Manual deletion command available.|

### 9. System Limitations
- Latency depends on device performance.
- No long-term memory or context retention (stateless).
- Speech accuracy drops in noisy environments.
- Currently supports English only (extendable).

### 10. Future Enhancements
| Area              | Planned Improvement             |
|-------------------|---------------------------------|
| Context Awareness | Store and recall user preferences locally. |
| Multi-language    | Add multilingual Whisper and TTS models. |
| Edge Optimization | Quantized models for smaller hardware. |
| Gesture Interaction | Integrate sensors or camera-based input. |
| Secure Federated Network | Allow “Nova” devices to learn collaboratively without data exchange. |

---
## 🧩 Summary
Nova’s System Analysis and Design demonstrates how to combine machine intelligence, ethical privacy, and aesthetic design into one functional, offline system.

It showcases:
- Modular architecture
- Local AI processing
- Minimalistic, human-centric interaction

**In short:** Nova isn’t just another assistant — it’s a blueprint for how personal technology should feel: private, calm, and truly personal.
