from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:kuak@localhost/growdb'
db = SQLAlchemy(app)

class Rol(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre_rol = db.Column(db.String(80), unique=True)

	def __init__(self, nombre_rol):
		self.nombre_rol = nombre_rol

	def __repr__(self):
		return '<Rol %r' % self.nombre_rol


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id'))
    rol = db.relationship(Rol, backref = db.backref('usuarios', lazy='dynamic'))

    def __init__(self, nombre_usuario, password):
        self.nombre_usuario = nombre_usuario
        self.password = password

    def autenticado(self):
    	return True

    def __repr__(self):
        return '<Usuario %r>' % self.nombre_usuario

class Perfil(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
	usuario = db.relationship(Usuario, backref = db.backref('perfiles', lazy='dynamic'))
	correo = db.Column(db.String(150))
	direccion = db.Column(db.String(150))
	telefono = db.Column(db.String(30))
	imagen = db.Column(db.String(200))

	def __init__(self, id_usuario, correo, direccion, telefono, imagen):
		self.id_usuario = id_usuario
		self.correo = correo
		self.direccion = direccion
		self.telefono = telefono
		self.imagen = imagen

	def __repr__(self):
		return '<Perfil %r' % self.correo
		

class Proyecto(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre_proyecto = db.Column(db.String(150))
	descripcion = db.Column(db.Text)
	fecha_inicio = db.Column(db.DateTime)
	fecha_fin = db.Column(db.DateTime)
	url_imagen = db.Column(db.String(250))
	id_usuario =  db.Column(db.Integer, db.ForeignKey('usuario.id'))
	usuario = db.relationship(Usuario, backref = db.backref('proyectos', lazy='dynamic'))

	def __init__(self, nombre_proyecto, descripcion, id_usuario, url_imagen = None, fecha_inicio = None, fecha_fin = None):
		self.nombre_proyecto = nombre_proyecto
		self.descripcion = descripcion
		self.url_imagen = url_imagen
		if fecha_inicio is None:
			fecha_inicio = datetime.utcnow()
		self.fecha_inicio = fecha_inicio
		if fecha_fin is None:
			fecha_fin = datetime.utcnow()
		self.fecha_fin = fecha_fin
		self.id_usuario = id_usuario
	
	def __repr__(self):
		return '<Proyecto %r>' % self.nombre_proyecto

class Comentario(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_usuario =  db.Column(db.Integer, db.ForeignKey('usuario.id'))
	usuario = db.relationship(Usuario, backref = db.backref('comentarios', lazy='dynamic'))
	id_proyecto = db.Column(db.Integer, db.ForeignKey('proyecto.id'))
	proyecto = db.relationship(Proyecto, backref = db.backref('comentarios', lazy='dynamic'))
	comentario = db.Column(db.String(250))

	def __init__(self, id_usuario, id_proyecto, comentario):
		self.id_usuario = id_usuario
		self.id_proyecto = id_proyecto
		self.comentario = comentario
		
	def __repr__(self):
			return '<Comentario %r' % self.comentario
