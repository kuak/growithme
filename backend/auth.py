from flask_oauth import OAuth
from model import db, Usuario
from sqlalchemy import and_

TWITTER_APP_ID = 'F3MOphJZbUNFn7UdbNnwFg'
TWITTER_APP_SECRET = 'rVBDWIAYEJvehgwgA3fgDiKlXcANNr9shwOjLsi6nA'
FACEBOOK_APP_ID = '523024991088570'
FACEBOOK_APP_SECRET = 'e75ff46a7b0bcd6b949db7fc14c7a1cf'

oauth = OAuth()

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=TWITTER_APP_ID,
    consumer_secret=TWITTER_APP_SECRET
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

def usuario_en_session(session):
    if 'user_id' in session:
        user = Usuario.query.get(session['user_id'])
        if user is None:
            return None
        return user
    return None

#def add_usuario_from_oauth_provider(req,provider):
#    if 'twitter' = provider:

def crear_usuario_request(request):
    print 'crear_usuario_request'
    print str(request.form)
    user = Usuario()
    user.nickname = request.form['nickname']
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.email = request.form['email']
    user.password = request.form['password']
    user.oauth_provider = 'growith.me'
    return user

def existe_usuario(user):
    u = Usuario.query.filter(Usuario.nickname==user.nickname).filter(Usuario.email==user.email).first()
    return u

