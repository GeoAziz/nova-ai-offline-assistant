"""
Minimal Flask interface for Nova status and memory.
"""
from flask import Flask, render_template_string, redirect, url_for
from memory_manager import load_memory, clear_memory

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
    </style>
</head>
<body>
    <div class="container">
        <h1>Nova Status & Memory</h1>
        <form method="POST" action="/clear_memory">
            <button class="clear-btn" type="submit">Clear Memory</button>
        </form>
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

@app.route("/")
def index():
    memory = load_memory()
    return render_template_string(TEMPLATE, memory=memory)

@app.route("/clear_memory", methods=["POST"])
def clear():
    clear_memory()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
