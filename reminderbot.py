import random
import tweepy
import click

def _get_random_quote():
    return random.choice(   _quotes)

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

    with open("OAUTH_TOKEN", "w") as f:
        click.echo(auth.access_token, file=f)
        click.echo(auth.access_token_secret, file=f)

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        click.echo(tweet.text)

@click.group()
def cli():
    pass

cli.add_command(authenticate)

if __name__ == '__main__':
    cli()