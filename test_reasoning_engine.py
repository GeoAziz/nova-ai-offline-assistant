"""
Unit tests for reasoning_engine fallback and backend selection.

These tests mock network calls to Open Web UI and Ollama to verify
that the reasoning engine honors the `use_open_webui` flag, retries
Open Web UI, and falls back to Ollama when necessary.
"""
import unittest
from unittest.mock import patch, MagicMock

import reasoning_engine
import requests


class TestReasoningEngine(unittest.TestCase):
    def setUp(self):
        # Ensure a clean config for each test
        reasoning_engine.CFG = {
            "open_webui_endpoint": "http://openwebui.local/api/generate",
            "ollama_endpoint": "http://ollama.local/api/generate",
            "use_open_webui": True,
            "open_webui_retries": 1,
            "open_webui_retry_delay": 0.0,
        }

    def make_resp(self, text=None, json_data=None, status=200):
        resp = MagicMock()
        resp.status_code = status
        if json_data is not None:
            resp.json.return_value = json_data
        else:
            resp.json.side_effect = ValueError("no json")
        resp.text = text or ""
        resp.raise_for_status.return_value = None
        return resp

    @patch("requests.post")
    def test_open_webui_success(self, mock_post):
        # Open Web UI returns a JSON response -> should be used
        ow_resp = self.make_resp(json_data={"response": "ow reply"})
        mock_post.return_value = ow_resp

        out = reasoning_engine.query_ollama("hello", use_open_webui=True)
        self.assertEqual(out, "ow reply")
        info = reasoning_engine.get_last_result_info()
        self.assertEqual(info["backend"], "open_webui")
        self.assertFalse(info["fallback"])

    @patch("requests.post")
    def test_open_webui_failure_fallback_to_ollama(self, mock_post):
        # First call to Open Web UI raises, second call (Ollama) returns text
        def side_effect(url, *args, **kwargs):
            if url == reasoning_engine.CFG["open_webui_endpoint"]:
                raise requests.exceptions.ConnectionError("ow down")
            if url == reasoning_engine.CFG["ollama_endpoint"]:
                return self.make_resp(json_data={"response": "ollama reply"})
            raise RuntimeError("unexpected url")

        mock_post.side_effect = side_effect

        out = reasoning_engine.query_ollama("fallback test", use_open_webui=True)
        self.assertEqual(out, "ollama reply")
        info = reasoning_engine.get_last_result_info()
        self.assertEqual(info["backend"], "ollama")
        self.assertTrue(info["fallback"])

    @patch("requests.post")
    def test_override_use_open_webui_false(self, mock_post):
        # Config enables OW, but explicit override disables it -> Ollama used
        def side_effect(url, *args, **kwargs):
            if url == reasoning_engine.CFG["ollama_endpoint"]:
                return self.make_resp(json_data={"response": "ollama only"})
            raise RuntimeError("unexpected url")

        mock_post.side_effect = side_effect

        out = reasoning_engine.query_ollama("no ow", use_open_webui=False)
        self.assertEqual(out, "ollama only")
        info = reasoning_engine.get_last_result_info()
        self.assertEqual(info["backend"], "ollama")
        self.assertFalse(info["fallback"])

    @patch("requests.post")
    def test_open_webui_api_key_from_env(self, mock_post):
        # Ensure that when OPEN_WEBUI_API_KEY env var is set, it's sent as a Bearer header
        ow_resp = self.make_resp(json_data={"response": "ow reply"})
        mock_post.return_value = ow_resp

        # Set environment variable and reset config
        import os
        os.environ["OPEN_WEBUI_API_KEY"] = "env-secret"
        reasoning_engine.CFG = {
            "open_webui_endpoint": "http://openwebui.local/api/generate",
            "ollama_endpoint": "http://ollama.local/api/generate",
            "use_open_webui": True,
            "open_webui_retries": 1,
        }

        out = reasoning_engine.query_ollama("hello", use_open_webui=True)
        self.assertEqual(out, "ow reply")

        # Ensure requests.post was called with headers containing Authorization: Bearer env-secret
        called_args, called_kwargs = mock_post.call_args
        headers = called_kwargs.get("headers", {})
        self.assertIn("Authorization", headers)
        self.assertEqual(headers["Authorization"], "Bearer env-secret")

        # Cleanup
        del os.environ["OPEN_WEBUI_API_KEY"]


if __name__ == "__main__":
    unittest.main()
