import unittest
from unittest.mock import patch

from interface import app
import interface


class TestInterfaceUI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    @patch('reasoning_engine.query_ollama')
    def test_backend_toggle_and_text_input(self, mock_query):
        # mock the reasoning engine to return a predictable reply
        mock_query.return_value = 'mocked reply'

        # set backend to open_webui via the form
        rv = self.client.post('/set_backend', data={'backend': 'open_webui'}, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

        # send a text input
        rv = self.client.post('/text_input', data={'user_text': 'hello'}, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'mocked reply', rv.data)

        # ensure the session note indicates which backend served the response
        # (UI note is set in session, so it's rendered)
        self.assertIn(b'Response served by', rv.data)

    def test_open_webui_send_includes_auth_header(self):
        # Simulate an API key configured via environment variables
        import os
        os.environ['OPEN_WEBUI_API_KEY'] = 'env-secret'
        os.environ['OPEN_WEBUI_API_KEY_STYLE'] = 'bearer'

        # Mock requests.post inside the interface module
        with patch('interface.requests.post') as mock_post:
            resp = mock_post.return_value
            resp.status_code = 200
            resp.json.return_value = {'response': 'ok'}
            resp.raise_for_status.return_value = None

            rv = self.client.post('/open_webui/send', data={'ow_prompt': 'hello'}, follow_redirects=True)
            self.assertEqual(rv.status_code, 200)

            # Ensure the header was sent
            called_args, called_kwargs = mock_post.call_args
            headers = called_kwargs.get('headers', {})
            self.assertIn('Authorization', headers)
            self.assertEqual(headers['Authorization'], 'Bearer env-secret')

        # Cleanup env
        del os.environ['OPEN_WEBUI_API_KEY']
        del os.environ['OPEN_WEBUI_API_KEY_STYLE']

    def test_open_webui_send_uses_x_api_key_style(self):
        # Simulate API key with x-api-key style
        import os
        os.environ['OPEN_WEBUI_API_KEY'] = 'env-secret-x'
        os.environ['OPEN_WEBUI_API_KEY_STYLE'] = 'x-api-key'

        with patch('interface.requests.post') as mock_post:
            resp = mock_post.return_value
            resp.status_code = 200
            resp.json.return_value = {'response': 'ok'}
            resp.raise_for_status.return_value = None

            rv = self.client.post('/open_webui/send', data={'ow_prompt': 'hello'}, follow_redirects=True)
            self.assertEqual(rv.status_code, 200)

            called_args, called_kwargs = mock_post.call_args
            headers = called_kwargs.get('headers', {})
            self.assertIn('X-API-Key', headers)
            self.assertEqual(headers['X-API-Key'], 'env-secret-x')

        # Cleanup
        del os.environ['OPEN_WEBUI_API_KEY']
        del os.environ['OPEN_WEBUI_API_KEY_STYLE']


if __name__ == '__main__':
    unittest.main()
