from flask import Flask
from flask import render_template
from flask import url_for
from flask import send_from_directory
#Uso del modelo
from backend.model import db, Usuario
from backend.model import Proyecto
#Manejo de archivos
#from flask_uploads import UploadSet, IMAGES, configure_uploads
#authenticate
from flask import g, session, request, flash, redirect
import backend.auth as auth

app = Flask(__name__)
app.secret_key = 'Kuak Team key'

#Carpeta para fotos de los proyectos
#fotos = UploadSet(name = 'fotos', extensions = IMAGES, default_dest=lambda app: "fotos/")
#configure_uploads(app, fotos)

#login 
@app.before_request
def before_request():
    g.user = auth.usuario_en_session(session)

@app.after_request
def after_request(response):
    db.session.remove()
    return response

@auth.twitter.tokengetter
def get_twitter_token():
    user = g.user
    if user is not None:
        return user.oauth_token, user.oauth_secret

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logintw")
def logintw():
    return auth.twitter.authorize(callback=url_for('callback_twitter', \
        next=request.args.get('next') or request.referrer or None))

@app.route('/callback_twitter')
@auth.twitter.authorized_handler
def callback_twitter(resp):
    next_url = request.args.get('next') or url_for('home')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    user = Usuario.query.filter_by(nickname=resp['screen_name']).first()

    if user is None:
        user = Usuario(resp['screen_name'],'')
        db.session.add(user)

    user.oauth_token = resp['oauth_token']
    user.oauth_token_secret = resp['oauth_token_secret']
    db.session.commit()

    session['user_id'] = user.id
    g.user = user
    flash('You were signed in')
    return redirect(next_url)

@app.route('/loginfb')
def loginfb():
    return auth.facebook.authorize(callback=url_for('callback_facebook',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route('/callback_facebook')
@auth.facebook.authorized_handler
def callback_facebook(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (request.args['error_reason'],request.args['error_description'])
    me = auth.facebook.get('/me')

    user = Usuario.query.filter_by(nickname=me.data['name']).first()
    if user is None:
        user = Usuario(me.data['name'],'')
        db.session.add(user)
    user.oauth_token = resp['access_token']
    db.session.commit()

    session['user_id'] = user.id
    g.user = user
    #return 'Logged in as id=%s name=%s redirect=%s' % (me.data['id'], me.data['name'], request.args.get('next'))
    return redirect(url_for('home'))

@auth.facebook.tokengetter
def get_facebook_oauth_token():
    return g.user.oauth_token

#- fin login

@app.route('/')
def home():
	proyectos = dProyecto.query.all()
	return render_template("home.html", proyectos = proyectos)

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
    #if request.method == 'POST' and 'foto' in request.files:
        #filename = fotos.save(request.files['foto'])
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
