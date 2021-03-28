from app import db
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user

class UsuarioModel(db.Model,UserMixin):
	__tablename__ = 'usuarioSistema'

	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String(150), nullable=False)
	email = db.Column(db.String(150),nullable=False)
	password = db.Column(db.String(255))
	endereco = db.Column(db.String(255))
	cidade = db.Column(db.String(255))
	estado = db.Column(db.String(50))
	cep = db.Column(db.String(10))
	tipoUsuario = db.Column(db.String(50))

	def __init__(self, nome,email,password,endereco,cidade,estado,cep,tipoUsuario):
		self.nome = nome
		self.email = email
		self.password = password
		self.endereco = endereco
		self.cidade = cidade
		self.estado = estado
		self.cep = cep
		self.tipoUsuario = tipoUsuario

	def __repr__(self):
		return '<UsuarioModel %r>' % self.nome
