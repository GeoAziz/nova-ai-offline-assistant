"""
Unit tests for Nova Flask interface.
"""
import unittest
from interface import app
from memory_manager import save_turn, clear_memory

class TestInterface(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        clear_memory()
        save_turn("Hello", "Hi there!")
        save_turn("What's the time?", "It's 2 PM.")

    def tearDown(self):
        clear_memory()

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Nova Status & Memory", response.data)
        self.assertIn(b"Hello", response.data)
        self.assertIn(b"Hi there!", response.data)

    def test_clear_memory(self):
        response = self.client.post("/clear_memory", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No conversation history.", response.data)

if __name__ == "__main__":
    unittest.main()
