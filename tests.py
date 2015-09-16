import unittest
import logging
import random
from mock import patch, Mock
from reminderbot import Reminderbot

class TestReminderbot(unittest.TestCase):
    def setUp(self):
        self.reminderbot = Reminderbot()

    def test_instantiation(self):
        result = Reminderbot()

    def test_get_random_quote_single(self):
        self.reminderbot._quotes = [
            "A quote"
        ]
        result = self.reminderbot._get_random_quote()
        self.assertEqual(result, "A quote")

    @patch("random.choice", Mock(side_effect=lambda quotes: quotes[0]))
    def test_get_random_quote_multi(self):
        self.reminderbot._quotes = [
            "A first quote",
            "A second quote"
        ]

        result = self.reminderbot._get_random_quote()
        self.assertEqual(result, "A first quote")

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	unittest.main()
