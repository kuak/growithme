from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/growdb'
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
    fist_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(32))
    nickname = db.Column(db.String(32))
    password = db.Column(db.String(254))
    direccion = db.Column(db.String(254))
    ciudad = db.Column(db.String(32))
    pais = db.Column(db.String(32))
    oauth_provider = db.Column(db.String(16))
    oauth_token = db.Column(db.String(254))
    oauth_token_secret = db.Column(db.String(512))
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id'))
    rol = db.relationship(Rol, backref = db.backref('usuarios', lazy='dynamic'))

    def autenticado(self):
    	return True

    def __repr__(self):
        return '<Usuario - id: '+str(self.id)+' nickname: '+self.nickname+'>' 

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
	meta = db.Column(db.Float)
	fecha_inicio = db.Column(db.DateTime)
	fecha_fin = db.Column(db.DateTime)
	url_imagen = db.Column(db.String(250))
	id_usuario =  db.Column(db.Integer, db.ForeignKey('usuario.id'))
	usuario = db.relationship(Usuario, backref = db.backref('proyectos', lazy='dynamic'))

	def __init__(self, nombre_proyecto, descripcion, meta, id_usuario, url_imagen = None, fecha_inicio = None, fecha_fin = None):
		self.nombre_proyecto = nombre_proyecto
		self.descripcion = descripcion
		self.meta = meta
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

class Recompensa(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre_recompensa = db.Column(db.String(150))
	id_proyecto = db.Column(db.Integer, db.ForeignKey('proyecto.id'))
	proyecto = db.relationship(Proyecto, backref = db.backref('recompensas', lazy='dynamic'))
	valor = db.Column(db.Float)
	descripcion = db.Column(db.String(250))

	def __init__(self, nombre_recompensa, id_proyecto, valor, descripcion):
		self.nombre_recompensa = nombre_recompensa
		self.id_proyecto = id_proyecto
		self.valor = valor
		self.descripcion = descripcion

	def __repr__(self):
		return '<Recompensa %r>' % self.nombre_recompensa
		

class Donacion(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	id_usuario =  db.Column(db.Integer, db.ForeignKey('usuario.id'))
	usuario = db.relationship(Usuario, backref = db.backref('donaciones', lazy='dynamic'))
	id_proyecto = db.Column(db.Integer, db.ForeignKey('proyecto.id'))
	proyecto = db.relationship(Proyecto, backref = db.backref('donaciones', lazy='dynamic'))
	valor = db.Column(db.Float, )
	fecha = db.Column(db.DateTime)
	tipo = db.Column(db.Integer)
	id_recompensa = db.Column(db.Integer, db.ForeignKey('recompensa.id'))
	recompensa = db.relationship(Recompensa, backref = db.backref('donaciones', lazy='dynamic'))

	def __init__(self, id_usuario, id_proyecto, valor, id_recompensa, fecha = None, tipo = 1):
		self.id_donacion = id_donacion
		self.id_usuario = id_usuario
		self.id_proyecto = id_proyecto
		self.valor = valor
		self.id_recompensa = id_recompensa
		if fecha is None:
			fecha = datetime.utcnow()
		self.fecha = fecha
		self.tipo = tipo

	def __repr__(self):
		return '<Donacion %r>' % str(self.id_donacion)
		

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
