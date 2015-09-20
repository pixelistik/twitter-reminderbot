import unittest
import logging
import random
from mock import patch, Mock
import reminderbot
import tweepy
import click
from click.testing import CliRunner

class TestReminderbot(unittest.TestCase):

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
    @patch("tweepy.API", Mock())
    @patch("click.prompt", Mock(return_value="12345"))
    @patch("click.echo", Mock())
    def test_authenticate(self):
        auth = Mock()
        tweepy.OAuthHandler.return_value = auth

        auth.access_token = "token"
        auth.access_token_secret = "token_secret"

        runner = CliRunner()
        result = runner.invoke(reminderbot.authenticate, ["key", "secret"])

        tweepy.OAuthHandler.assert_called_once_with("key", "secret")
        auth.get_authorization_url.assert_called_once_with()
        auth.get_access_token.assert_called_once_with("12345")

    @patch("reminderbot._get_random_quote", Mock(return_value="A tweeted quote"))
    @patch("tweepy.API", Mock())
    def test_tweet_random_quote(self):
        api_mock = Mock()
        tweepy.API.return_value = api_mock

        runner = CliRunner()
        result = runner.invoke(reminderbot.tweet, catch_exceptions=False)

        api_mock.update_status.assert_called_once_with("A tweeted quote")

    def test_read_quotes_from_file(self):
        pass

if __name__ == '__main__':
	unittest.main()
