"""
Minimal Flask interface for Nova status and memory.
"""

from flask import Flask, render_template_string, redirect, url_for
from memory_manager import load_memory, clear_memory, suggest_routine, get_routines, add_reminder, get_reminders
from text_to_speech import get_available_voices

app = Flask(__name__)




TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Nova Status</title>
    <style>
        body { font-family: sans-serif; background: #f7f7f7; }
        .container { max-width: 600px; margin: 40px auto; background: #fff; padding: 24px; border-radius: 8px; box-shadow: 0 2px 8px #ccc; }
        h1 { color: #2a2a2a; }
        .turn { margin-bottom: 16px; }
        .user { color: #0074d9; }
        .nova { color: #ff851b; }
        .clear-btn { background: #e74c3c; color: #fff; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
        .routine { background: #eafaf1; color: #2a7b4f; padding: 12px; border-radius: 6px; margin-bottom: 18px; }
        .reminder-btn { background: #2a7b4f; color: #fff; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; margin-left: 8px; }
        .reminders { background: #fffbe6; color: #b8860b; padding: 10px; border-radius: 6px; margin-bottom: 18px; }
        .tts-select { background: #eaf1fa; color: #2a2a2a; padding: 10px; border-radius: 6px; margin-bottom: 18px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Nova Status & Memory</h1>
        <div class="tts-select">
            <form method="POST" action="/set_tts_voice">
                <strong>TTS Voice:</strong>
                <select name="voice">
                    {% for v in voices %}
                        <option value="{{ v.name }}" {% if v.name == selected_voice %}selected{% endif %}>{{ v.name }} ({{ v.language }}, {{ v.style }})</option>
                    {% endfor %}
                </select>
                <button type="submit">Set Voice</button>
            </form>
        </div>
        <div class="routine">
            <strong>Routine Suggestion:</strong> {{ routine_suggestion }}
            {% for routine in routines %}
                <form method="POST" action="/add_reminder" style="display:inline;">
                    <input type="hidden" name="routine" value="{{ routine }}">
                    <button class="reminder-btn" type="submit">Set Reminder for '{{ routine }}'</button>
                </form>
            {% endfor %}
        </div>
        <div class="reminders">
            <strong>Active Reminders:</strong>
            {% if reminders %}
                {{ reminders|join(", ") }}
            {% else %}
                None
            {% endif %}
        </div>
        <form method="POST" action="/clear_memory">
            <button class="clear-btn" type="submit">Clear Memory</button>
        </form>
        <h2>Talk to Nova (Text)</h2>
        <form method="POST" action="/text_input">
            <input type="text" name="user_text" placeholder="Type your message..." style="width:80%;padding:8px;">
            <button type="submit">Send</button>
        </form>
        {% if text_response %}
            <div class="nova" style="margin-top:16px;"><strong>Nova:</strong> {{ text_response }}</div>
        {% endif %}
        <h2>Recent Conversation</h2>
        {% for turn in memory %}
            <div class="turn">
                <div class="user"><strong>User:</strong> {{ turn.user }}</div>
                <div class="nova"><strong>Nova:</strong> {{ turn.nova }}</div>
            </div>
        {% else %}
            <p>No conversation history.</p>
        {% endfor %}
    </div>
</body>
</html>
"""




from flask import session
app.secret_key = "nova_secret_key"

@app.route("/")
def index():
    memory = load_memory()
    routine_suggestion = suggest_routine()
    routines = get_routines()
    reminders = get_reminders()
    voices = get_available_voices()
    selected_voice = session.get("tts_voice", "en_US")
    text_response = session.pop("text_response", None)
    return render_template_string(TEMPLATE, memory=memory, routine_suggestion=routine_suggestion, routines=routines, reminders=reminders, voices=voices, selected_voice=selected_voice, text_response=text_response)
@app.route("/text_input", methods=["POST"])
def text_input():
    from flask import request
    user_text = request.form.get("user_text")
    response = ""
    if user_text:
        # Reasoning engine
        from reasoning_engine import query_ollama
        try:
            response = query_ollama(user_text, endpoint="http://localhost:11434/api/generate", model="llama3")
        except Exception as e:
            response = f"Error: {e}"
        session["text_response"] = response
    return redirect(url_for('index'))

@app.route("/set_tts_voice", methods=["POST"])
def set_tts_voice():
    from flask import request
    voice = request.form.get("voice")
    if voice:
        session["tts_voice"] = voice
    return redirect(url_for('index'))

@app.route("/add_reminder", methods=["POST"])
def add_reminder_route():
    from flask import request
    routine = request.form.get("routine")
    if routine:
        add_reminder(routine)
    return redirect(url_for('index'))

@app.route("/clear_memory", methods=["POST"])
def clear():
    clear_memory()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
