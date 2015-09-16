import unittest
import logging
import random
from mock import patch, Mock
import reminderbot
import tweepy
import click
from click.testing import CliRunner

class TestReminderbot(unittest.TestCase):
    def __init__(self):
        self.open_name = "%s.open" % __name__

    def test_get_random_quote_single(self):
        reminderbot._quotes = [
            "A quote"
        ]
        result = reminderbot._get_random_quote()
        self.assertEqual(result, "A quote")

    @patch("random.choice", Mock(side_effect=lambda quotes: quotes[0]))
    def test_get_random_quote_multi(self):
        reminderbot._quotes = [
            "A first quote",
            "A second quote"
        ]

        result = reminderbot._get_random_quote()
        self.assertEqual(result, "A first quote")

    @patch("tweepy.OAuthHandler", Mock())
    @patch("click.prompt", Mock(return_value="12345"))
    @patch(self.open_name, Mock())
    def test_authenticate(self):
        auth = Mock()
        tweepy.OAuthHandler.return_value = auth

        token_file = Mock()
        open.return_value = token_file

        auth.access_token = "token"
        auth.access_token_secret = "token_secret"

        runner = CliRunner()
        result = runner.invoke(reminderbot.authenticate, ["key", "secret"])

        tweepy.OAuthHandler.assert_called_once_with("key", "secret")
        auth.get_authorization_url.assert_called_once_with()
        auth.get_access_token.assert_called_once_with("12345")

        token_file.assert_called_once_with("token\ntoken_secret")



if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	unittest.main()
