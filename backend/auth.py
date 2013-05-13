from flask_oauth import OAuth

SECRET_TWITTER_KEY = ''

oauth = OAuth()

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='F3MOphJZbUNFn7UdbNnwFg',
    consumer_secret='rVBDWIAYEJvehgwgA3fgDiKlXcANNr9shwOjLsi6nA'
)