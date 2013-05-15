from flask import Flask
from flask import render_template
from flask import url_for
from flask import send_from_directory
from backend.model import Proyecto

app = Flask(__name__)

@app.route('/')
def home():
	proyectos = Proyecto.query.all()
	return render_template("home.html", proyectos = proyectos)

@app.route("/login")
def login():
    return render_template("login.html")

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
