"""
Manages local memory, conversation history, and privacy controls.
"""

import json
import os

MEMORY_FILE = "logs/conversation_history.json"
MEMORY_LIMIT = 20

def load_memory():
	if not os.path.exists(MEMORY_FILE):
		return []
	with open(MEMORY_FILE, "r") as f:
		try:
			return json.load(f)
		except Exception:
			return []

def save_turn(user_text: str, nova_response: str):
	memory = load_memory()
	memory.append({"user": user_text, "nova": nova_response})
	if len(memory) > MEMORY_LIMIT:
		memory = memory[-MEMORY_LIMIT:]
	with open(MEMORY_FILE, "w") as f:
		json.dump(memory, f, indent=2)

def clear_memory():
	if os.path.exists(MEMORY_FILE):
		os.remove(MEMORY_FILE)
	print("Conversation memory cleared.")
