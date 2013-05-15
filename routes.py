from flask import Flask
from flask import render_template
from flask import url_for
from flask import send_from_directory
from backend.model import db
from backend.model import Proyecto
#authenticate
from flask import g, session, request, flash, redirect
from backend.auth import twitter, facebook

app = Flask(__name__)
app.secret_key = 'Kuak Team key'

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        #g.user = User.query.get(session['user_id'])
        print 'before_request:'
        print 'User Id: ' + session['user_id']
        print 'oauth_token: '
        print session['oauth_token']
        print 'oauth_token_secret: '
        print session['oauth_token_secret']

@app.after_request
def after_request(response):
    #db_session.remove()
    return response

@twitter.tokengetter
def get_twitter_token():
    user = g.user
    if user is not None:
        return user.oauth_token, user.oauth_secret

@app.route('/')
def home():
	proyectos = Proyecto.query.all()
	return render_template("home.html", proyectos = proyectos)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logintw")
def logintw():
	return twitter.authorize(callback=url_for('callback_twitter', \
		next=request.args.get('next') or request.referrer or None))

@app.route('/callback_twitter')
@twitter.authorized_handler
def callback_twitter(resp):
    next_url = request.args.get('next') or url_for('home')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    user = None

    #user = User.query.filter_by(name=resp['screen_name']).first()

    # user never signed on
    if user is None:
    	print resp['screen_name']
        #user = User(resp['screen_name'])
        #db_session.add(user)

    # in any case we update the authenciation token in the db
    # In case the user temporarily revoked access we will have
    # new tokens here.
    #user.oauth_token = resp['oauth_token']
    #user.oauth_secret = resp['oauth_token_secret']
    print 'oauth_token'
    print resp['oauth_token']
    print 'oauth_token_secret'
    print resp['oauth_token_secret']
    #db_session.commit()

    session['user_id'] = resp['screen_name'] #user.id
    session['oauth_token_secret'] = resp['oauth_token_secret']
    session['oauth_token'] = resp['oauth_token']
    print 'callback_twitter: user id: '+ resp['screen_name'] #user.id
    flash('You were signed in')
    return redirect(next_url)

@app.route('/loginfb')
def loginfb():
	return facebook.authorize(callback=url_for('callback_facebook',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route('/callback_facebook')
@facebook.authorized_handler
def callback_facebook(resp):
	if resp is None:
		return 'Access denied: reason=%s error=%s' % (request.args['error_reason'],request.args['error_description'])
	session['oauth_token'] = (resp['access_token'], '')
	print str(resp)
	me = facebook.get('/me')
	return 'Logged in as id=%s name=%s redirect=%s' % (me.data['id'], me.data['name'], request.args.get('next'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
	return render_template("contact.html")

@app.route("/register")
def register():
	return render_template("register.html")

##Rutas para usuarios registrados
@app.route("/new-project")
def new_project():
	return render_template("new_project.html")

@app.route("/add-project", methods=['POST'])
def add_project():
    new_pro = Proyecto(request.form['nombre_proyecto'], request.form['descripcion'], 1)
    db.session.add(new_pro)
    db.session.commit()
    flash('Nuevo proyecto ha sido guardado con exito')
    return redirect(url_for('home'))

@app.route("/projects")
def perfil():
    return render_template("projects.html")

#Estas rutas se colocan para correr la aplicacion localamente.
#En produccion el servidor web se encargara de direccionar el contenido estatico.
@app.route("/css/<path:filename>")
def css(filename):
	return send_from_directory('static/css/',filename)

@app.route("/js/<path:filename>")
def js(filename):
	return send_from_directory('static/js/',filename)

@app.route('/img/<path:filename>')
def image(filename):
	return send_from_directory('static/img/',filename)

#Verifica si se corre como un modulo o como una aplicacion principal, utilizado cuando se corre la aplicacion localmente
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
