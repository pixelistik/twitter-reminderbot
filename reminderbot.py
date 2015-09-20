import random
import tweepy
import click

def _get_random_quote():
    return random.choice(_quotes)

@click.command()
@click.argument("consumer_key")
@click.argument("consumer_secret")
def authenticate(consumer_key, consumer_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    try:
        url = auth.get_authorization_url()
    except tweepy.TweepError:
        click.echo("Failed to get request token.")

    click.echo("Setting up authentication. Please visit this URL:")
    click.echo(url)
    verifier = click.prompt("Enter the authorisation PIN from Twitter")

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        click.echo("Error! Failed to get access token.")

    with open("OAUTH_CONSUMER", "w") as f:
        click.echo(consumer_key, file=f)
        click.echo(consumer_secret, file=f)

    with open("OAUTH_TOKEN", "w") as f:
        click.echo(auth.access_token, file=f)
        click.echo(auth.access_token_secret, file=f)

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        click.echo(tweet.text)

@click.command()
def tweet():
    with open("OAUTH_CONSUMER", "r") as f:
        lines = f.readlines()
        consumer_key = lines[0]
        consumer_secret = lines[1]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    with open("OAUTH_TOKEN", "r") as f:
        lines = f.readlines()
        access_token = lines[0]
        access_token_secret = lines[1]

    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    api.update_status(_get_random_quote())

@click.group()
def cli():
    pass

cli.add_command(authenticate)
cli.add_command(tweet)

if __name__ == '__main__':
    cli()