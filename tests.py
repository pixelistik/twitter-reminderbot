import unittest
import logging
from reminderbot import Reminderbot

class TestReminderbot(unittest.TestCase):
    def test_instantiation(self):
        result = Reminderbot()

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	unittest.main()