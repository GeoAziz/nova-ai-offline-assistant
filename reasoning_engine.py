"""Reasoning engine abstraction.

This module routes reasoning requests to one of the available local
backends (Ollama by default). It will optionally forward requests to an
Open Web UI HTTP endpoint when enabled in `config/config.yaml`.

Public API: query_ollama(prompt, endpoint=None, model=None)
  - For backwards compatibility this function name is kept, but it will
	consult config to determine which backend to call.
"""

import os
import yaml
import requests
from typing import Optional


def _load_cfg() -> dict:
	try:
		with open(os.path.join("config", "config.yaml"), "r") as f:
			return yaml.safe_load(f) or {}
	except Exception:
		return {}


CFG = _load_cfg()

# Store info about the last reasoning call so UI can display notices (non-persistent)
LAST_RESULT = {"backend": None, "fallback": False}


def query_ollama(prompt: str, endpoint: Optional[str] = None, model: Optional[str] = None, use_open_webui: Optional[bool] = None) -> str:
	"""Send prompt to reasoning backend and return textual response.

	If `use_open_webui` is true in config, this will POST {"prompt": prompt}
	to the configured `open_webui_endpoint` and return a best-effort text
	from the response. Otherwise it will send to Ollama using the standard
	payload {"model": model, "prompt": prompt}.
	"""
	# If caller provided explicit override, use it; otherwise fall back to config
	use_ow = CFG.get("use_open_webui", False) if use_open_webui is None else bool(use_open_webui)

	# Allow override via kwargs, otherwise use config or defaults
	ollama_endpoint = endpoint or CFG.get("ollama_endpoint", "http://localhost:11434/api/generate")
	ollama_model = model or CFG.get("ollama_model", "llama3")
	open_webui_endpoint = CFG.get("open_webui_endpoint", f"http://localhost:{CFG.get('open_webui_port', 3000)}/api/generate")
	# Prefer explicit environment variables for secrets; fall back to config file
	open_webui_api_key = os.environ.get("OPEN_WEBUI_API_KEY") or CFG.get("open_webui_api_key")
	open_webui_api_key_style = CFG.get("open_webui_api_key_style", "bearer")
	ollama_api_key = os.environ.get("OLLAMA_API_KEY") or CFG.get("ollama_api_key")
	ollama_api_key_style = CFG.get("ollama_api_key_style", "bearer")

	def _parse_response_text(resp):
		try:
			data = resp.json()
			return data.get("response") or data.get("output") or data.get("text") or str(data)
		except Exception:
			return resp.text

	# Try Open Web UI first if requested, but fall back to Ollama on any failure.
	try:
		LAST_RESULT["backend"] = None
		LAST_RESULT["fallback"] = False
		if use_ow:
			# configurable retries and delay
			retries = int(CFG.get("open_webui_retries", 2))
			delay = float(CFG.get("open_webui_retry_delay", 1.0))
			ow_success = False
			ow_err = None
			for attempt in range(1, retries + 1):
				try:
					headers = {}
					if open_webui_api_key:
						if open_webui_api_key_style and open_webui_api_key_style.lower() == "x-api-key":
							headers["X-API-Key"] = open_webui_api_key
						else:
							headers["Authorization"] = f"Bearer {open_webui_api_key}"
					resp = requests.post(open_webui_endpoint, json={"prompt": prompt}, timeout=15, headers=headers)
					resp.raise_for_status()
					LAST_RESULT["backend"] = "open_webui"
					LAST_RESULT["fallback"] = False
					return _parse_response_text(resp)
				except Exception as e:
					ow_err = e
					# small backoff before retrying
					if attempt < retries:
						try:
							import time
							time.sleep(delay * attempt)
						except Exception:
							pass
			# If we reach here, Open Web UI failed all attempts
			print("Open Web UI call failed after retries, falling back to Ollama:", ow_err)
			LAST_RESULT["fallback"] = True

		# Default / fallback: call Ollama
		payload = {"model": ollama_model, "prompt": prompt}
		headers = {}
		if ollama_api_key:
			if ollama_api_key_style and ollama_api_key_style.lower() == "x-api-key":
				headers["X-API-Key"] = ollama_api_key
			else:
				headers["Authorization"] = f"Bearer {ollama_api_key}"
		resp = requests.post(ollama_endpoint, json=payload, timeout=15, headers=headers)
		resp.raise_for_status()
		LAST_RESULT["backend"] = "ollama"
		return _parse_response_text(resp)
	except Exception as e:
		print("Reasoning engine error:", e)
		return ""


def get_last_result_info() -> dict:
	"""Return information about the last reasoning call.

	Returns a dict with keys: 'backend' ("open_webui" or "ollama" or None)
	and 'fallback' (bool) indicating whether a fallback occurred.
	"""
	return dict(LAST_RESULT)
