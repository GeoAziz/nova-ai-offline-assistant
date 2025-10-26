"""
Unit tests for led_feedback.py
"""
import unittest
from unittest.mock import patch, MagicMock
import led_feedback

class TestLedFeedback(unittest.TestCase):
    @patch('led_feedback.PixelStrip', autospec=True)
    def test_setup_led_available(self, mock_strip):
        mock_strip.return_value = MagicMock()
        strip = led_feedback.setup_led()
        self.assertIsNotNone(strip)

    def test_setup_led_unavailable(self):
        # Simulate missing rpi_ws281x
        with patch('led_feedback.PixelStrip', None):
            strip = led_feedback.setup_led()
            self.assertIsNone(strip)

    @patch('led_feedback.PixelStrip', autospec=True)
    @patch('led_feedback.Color', autospec=True)
    def test_set_led_state(self, mock_color, mock_strip):
        strip = MagicMock()
        led_feedback.set_led_state(strip, 'listening')
        led_feedback.set_led_state(strip, 'thinking')
        led_feedback.set_led_state(strip, 'speaking')
        led_feedback.set_led_state(strip, 'idle')
        # Should not raise exceptions

    def test_set_led_state_none(self):
        # Should do nothing if strip is None
        led_feedback.set_led_state(None, 'listening')

if __name__ == '__main__':
    unittest.main()
