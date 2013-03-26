from flask import Flask
from flask import render_template
from flask import url_for
from flask import send_from_directory

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/login")
def login():
    return render_template("login.html")

# Estas rutas se colocan para correr la aplicación localamente.
# En producción el servidor web se encargará de direccionar el contenido estático.
@app.route("/css/<path:filename>")
def css(filename):
	return send_from_directory('static/css/',filename)

@app.route("/js/<path:filename>")
def js(filename):
	return send_from_directory('static/js/',filename)

@app.route('/img/<path:filename>')
def image(filename):
	return send_from_directory('static/img/',filename)

#Verifica si se corre como un módulo o como una aplicación principal, utilizado cuando se corre la aplicación localmente
if __name__ == '__main__':
    app.run(debug=True)
