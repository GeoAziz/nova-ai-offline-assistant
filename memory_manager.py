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

def get_routines():
	"""
	Analyze memory for recurring requests (simple keyword-based routine detection).
	Returns a list of detected routines (e.g., reminders, meetings).
	"""
	memory = load_memory()
	routines = {}
	for turn in memory:
		user_text = turn.get("user", "").lower()
		# Simple keyword detection for routines
		for keyword in ["remind", "meeting", "drink water", "study", "exercise"]:
			if keyword in user_text:
				routines[keyword] = routines.get(keyword, 0) + 1
	# Return routines that occurred more than once
	return [k for k, v in routines.items() if v > 1]

def suggest_routine():
	"""
	Suggest a routine to the user based on detected patterns.
	"""
	routines = get_routines()
	if routines:
		return f"You seem to often mention: {', '.join(routines)}. Would you like a regular reminder?"
	return "No recurring routines detected yet."

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


# Reminder management
REMINDER_FILE = "logs/active_reminders.json"

import datetime

def add_reminder(routine: str, time_str: str = None):
	reminders = get_reminders()
	reminder = {"routine": routine}
	if time_str:
		reminder["time"] = time_str
	if reminder not in reminders:
		reminders.append(reminder)
	with open(REMINDER_FILE, "w") as f:
		json.dump(reminders, f, indent=2)

def get_reminders():
	if not os.path.exists(REMINDER_FILE):
		return []
	with open(REMINDER_FILE, "r") as f:
		try:
			return json.load(f)
		except Exception:
			return []

def check_due_reminders():
	"""
	Returns a list of reminders that are due (time <= now).
	"""
	now = datetime.datetime.now().strftime("%H:%M")
	due = []
	for r in get_reminders():
		if "time" in r and r["time"] == now:
			due.append(r)
	return due
