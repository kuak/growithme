from flask_oauth import OAuth

FACEBOOK_APP_ID = '523024991088570'
FACEBOOK_APP_SECRET = 'e75ff46a7b0bcd6b949db7fc14c7a1cf'

oauth = OAuth()

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='F3MOphJZbUNFn7UdbNnwFg',
    consumer_secret='rVBDWIAYEJvehgwgA3fgDiKlXcANNr9shwOjLsi6nA'
)

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)