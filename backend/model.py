from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kuak@localhost/growdb'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, nombre_usuario, password):
        self.nombre_usuario = nombre_usuario
        self.password = password

    def autenticado(self):
    	return True

    def __repr__(self):
        return '<Usuario %r>' % self.nombre_usuario

class Proyecto(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre_proyecto = db.Column(db.String(150))
	descripcion = db.Column(db.Text)
	fecha_inicio = db.Column(db.DateTime)
	fecha_fin = db.Column(db.DateTime)
	id_usuario =  db.Column(db.Integer, db.ForeignKey('usuario.id'))
	usuario = db.relationship(Usuario, backref = db.backref('proyectos', lazy='dynamic'))

	def __init__(self, nombre_proyecto, descripcion, id_usuario, fecha_inicio = None, fecha_fin = None):
		self.nombre_proyecto = nombre_proyecto
		self.descripcion = descripcion
		if fecha_inicio is None:
			fecha_inicio = datetime.utcnow()
		self.fecha_inicio = fecha_inicio
		if fecha_fin is None:
			fecha_fin = datetime.utcnow()
		self.fecha_fin = fecha_fin
		self.id_usuario = id_usuario
	
	def __repr__(self):
		return '<Proyecto %r>' % self.nombre_proyecto