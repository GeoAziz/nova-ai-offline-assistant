"""
Handles communication with Ollama local LLM for reasoning.
"""

import requests

def query_ollama(prompt: str, endpoint: str = "http://localhost:11434/api/generate", model: str = "llama3") -> str:
	"""
	Sends prompt to Ollama local endpoint and returns response.
	Args:
		prompt (str): User input to send to LLM.
		endpoint (str): Ollama API endpoint.
		model (str): Model name to use.
	Returns:
		str: LLM response text.
	"""
	payload = {
		"model": model,
		"prompt": prompt
	}
	try:
		response = requests.post(endpoint, json=payload)
		response.raise_for_status()
		data = response.json()
		return data.get("response", "")
	except Exception as e:
		print("Ollama reasoning error:", e)
		return ""
