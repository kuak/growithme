from flask import Flask
from flask import render_template
from flask import url_for
from flask import send_from_directory
#Uso del modelo
from backend.model import db, Usuario
from backend.model import Proyecto
#Uso de helpers
import backend.helpers as helpers 
#Manejo de archivos
from flaskext.uploads import UploadSet, IMAGES, configure_uploads
#authenticate
from flask import g, session, request, flash, redirect
import backend.auth as auth

app = Flask(__name__)
app.secret_key = 'Kuak Team key'

#Carpeta para fotos de los proyectos
imagenes = UploadSet(name = 'fotos', extensions = IMAGES, default_dest=lambda app: "fotos/")
configure_uploads(app, imagenes)

#login 
@app.before_request
def before_request():
    g.user = auth.usuario_en_session(session)
    #print str(g.user)

@app.after_request
def after_request(response):
    db.session.remove()
    return response

@auth.twitter.tokengetter
def get_twitter_token():
    user = g.user
    if user is not None:
        return user.oauth_token, user.oauth_secret

@app.route("/login",methods=['GET','POST'])
def login():
    if g.user is None:
        if request.method == 'GET':
            return render_template("login.html")
        else:
            user = Usuario.query.filter(Usuario.email==request.form['email']).filter(Usuario.password==request.form['password']).first()
            if user is None:
                return error_login('Usuario no existe')
            else:
                session['user_id'] = user.id
                session['oauth_provider'] = user.oauth_provider
                g.user = user
                return redirect(url_for('home'))
    else:
        return "Usuario logueado "+str(g.user.nickname)


@app.route("/logintw")
def logintw():
    return auth.twitter.authorize(callback=url_for('callback_twitter', \
        next=request.args.get('next') or request.referrer or None))

@app.route('/callback_twitter')
@auth.twitter.authorized_handler
def callback_twitter(resp):
    next_url = request.args.get('next') or url_for('home')
    if resp is None:
        error_login(u'You denied the request to sign in.')
        return redirect(next_url)

    user = Usuario.query.filter_by(nickname=resp['screen_name']).first()

    if user is None:
        user = Usuario()
        user.nickname = resp['screen_name']
        user.oauth_provider = 'twitter'
        db.session.add(user)

    user.oauth_token = resp['oauth_token']
    user.oauth_token_secret = resp['oauth_token_secret']

    db.session.commit()

    session['user_id'] = user.id
    session['oauth_provider'] = user.oauth_provider
    g.user = user

    return redirect(url_for('home'))

@app.route('/loginfb')
def loginfb():
    return auth.facebook.authorize(callback=url_for('callback_facebook',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route('/callback_facebook')
@auth.facebook.authorized_handler
def callback_facebook(resp):
    if resp is None:
        return error_login('Access denied: reason=%s error=%s' % (request.args['error_reason'],request.args['error_description']))

    user_tmp = Usuario()
    user_tmp.oauth_token = resp['access_token']
    g.user = user_tmp

    me = auth.facebook.get('/me')
    user = Usuario.query.filter(Usuario.nickname==me.data['name']).filter(Usuario.email==me.data['email']).first()

    if user is None:
        user = Usuario()
        user.email = me.data['email']
        user.oauth_provider = "facebook"
        user.nickname = me.data['name']
        db.session.add(user)
    user.oauth_token = resp['access_token']
    db.session.commit()

    session['user_id'] = user.id
    session['oauth_provider'] = user.oauth_provider
    g.user = user
    return redirect(url_for('home'))

@auth.facebook.tokengetter
def get_facebook_oauth_token():
    return (g.user.oauth_token,'')

#- fin login

@app.route('/')
def home():
	proyectos = Proyecto.query.all()
    for proy in proyectos:
        proy.days = helpers.fun_daysDiff(proy.fecha_inicio, proy.fecha_fin)
    return render_template("home.html", proyectos = proyectos)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
	return render_template("contact.html")

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        user = auth.crear_usuario_request(request)
        if auth.existe_usuario(user) is None:
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            session['oauth_provider'] = user.oauth_provider
            g.user = user
            return redirect(url_for('home'))
        else:
            return error_login('Usuario ya existe')

def error_login(msj):
    g.user = None
    return "Error intentando logear [%s]"%msj

##Rutas para usuarios registrados
@app.route("/my-projects")
def my_projects():
    proyectos = Proyecto.query.all()
    for pro in proyectos:
        pro.days = helpers.fun_daysDiff(pro.fecha_inicio, pro.fecha_fin)
    return render_template("my_projects.html", proyectos = proyectos)

@app.route("/new-project")
def new_project():
	return render_template("new_project.html")

@app.route("/modify-project/<path:_id>")
def modify_project(_id):
    proyecto = Proyecto.query.filter_by(id = _id).first()
    return render_template("modify_project.html", proyecto = proyecto)

@app.route("/add-project", methods=['POST'])
def add_project():
    new_pro = Proyecto(request.form['nombre_proyecto'], request.form['descripcion'], request.form['meta'], 1)
    
    if request.method == 'POST' and 'foto' in request.files:
        filename = imagenes.save(request.files['foto'])
        new_pro.url_imagen = filename
    db.session.add(new_pro)
    db.session.commit()

    flash("Nuevo proyecto guardado con exito")
    return redirect(url_for('my_projects'))

@app.route("/upd-project", methods=['POST'])
def upd_project():
    upd_pro = Proyecto.query.filter_by(id = request.form['id']).first()
    upd_pro.nombre_proyecto = request.form['nombre_proyecto']
    upd_pro.descripcion = request.form['descripcion']
    upd_pro.meta = request.form['meta']
    db.session.commit()
    flash("Proyecto guardado con exito")
    return redirect(url_for('my_projects'))

@app.route("/projects")
def projects():
    proyectos = Proyecto.query.all()
    for pro in proyectos:
        pro.days = helpers.fun_daysDiff(pro.fecha_inicio, pro.fecha_fin)
    return render_template("projects.html", proyectos = proyectos)

@app.route("/project/<path:_id>")
def project(_id):
    proyecto = Proyecto.query.filter_by(id = _id).first()
    proyecto.days = helpers.fun_daysDiff(proyecto.fecha_inicio, proyecto.fecha_fin)
    return render_template("project.html", proyecto = proyecto)

#Estas rutas se colocan para correr la aplicacion localamente.
#En produccion el servidor web se encargara de direccionar el contenido estatico.
@app.route("/css/<path:filename>")
def css(filename):
    return send_from_directory('static/css/',filename)

@app.route("/font-awesome/css/<path:filename>")
def css(filename):
    return send_from_directory('static/font-awesome/css/',filename)

@app.route("/font-awesome/font/<path:filename>")
def css(filename):
    return send_from_directory('static/font-awesome/font/',filename)    

@app.route("/font-awesome/less/<path:filename>")
def css(filename):
    return send_from_directory('static/font-awesome/less/',filename)
    
@app.route("/css/<path:filename>")
def css(filename):
	return send_from_directory('static/css/',filename)

@app.route("/font-awesome/css/<path:filename>")
def css(filename):
	return send_from_directory('static/font-awesome/css/',filename)

@app.route("/font-awesome/font/<path:filename>")
def css(filename):
	return send_from_directory('static/font-awesome/font/',filename)	
	
@app.route("/font-awesome/less/<path:filename>")
def css(filename):
	return send_from_directory('static/font-awesome/less/',filename)
	
	
@app.route("/js/<path:filename>")
def js(filename):
	return send_from_directory('static/js/',filename)

@app.route('/img/<path:filename>')
def image(filename):
	return send_from_directory('static/img/',filename)

@app.route('/fotos/<path:filename>')
def fotos(filename):
    return send_from_directory('fotos/',filename)

#Verifica si se corre como un modulo o como una aplicacion principal, utilizado cuando se corre la aplicacion localmente
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
