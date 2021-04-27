from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db, login_manager
from app.models.PessoaModel import Pessoa
from app.models.UsuarioModel import UsuarioModel
from app.models.ProdutoModel import ProdutoModel
from app.controllers.login.login import requires_roles 
# from app.models import User, requires_roles
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/cadastrarUsuario')
# @login_required
def cadastrarUsuario():
	return render_template('cadastroUsuario.html')


@app.route('/salvar_cadastro',methods=['POST'])
@login_required
def salvar_cadastro():
	nome = request.form.get('nome')
	email = request.form.get('email')
	password = generate_password_hash(request.form["password"])
	endereco = request.form.get('endereco')
	cidade = request.form.get('cidade')
	estado = request.form.get('estado')
	cep = request.form.get('cep')
	tipoUsuario = request.form.get('tipoUsuario')

	usuario = UsuarioModel(nome,email,password,endereco,cidade,estado,cep,tipoUsuario)

	db.session.add(usuario)
	db.session.commit()

	usuarios = UsuarioModel.query.all()
	return render_template('listarUsuarios.html', usuarios=usuarios)
    
@app.route('/listarUsuarios')
@login_required
@requires_roles('Cliente')
def listarUsuarios():
	usuarios = UsuarioModel.query.all()
	return render_template('listarUsuarios.html', usuarios=usuarios)


@app.route('/deletarUsuario/<int:id>')
@login_required
def deletarUsuario(id=0):
	usuario = UsuarioModel.query.filter_by(id=id).first()

	return render_template('deletarUsuario.html', usuario=usuario)

    
@app.route('/savedeletarUsuario',methods=['POST'])
@login_required
def savedeletarUsuario():
	id = int(request.form.get('id'))

	usuario = usuarios = UsuarioModel.query.filter_by(id=id).first()
	
	db.session.delete(usuario)
	db.session.commit()
	
	usuarios = UsuarioModel.query.all()
	return render_template('listarUsuarios.html', usuarios=usuarios)

@app.route('/editarUsuario/<int:id>')
@login_required
def editarUsuario(id=0):
	usuario = usuarios = UsuarioModel.query.filter_by(id=id).first()
	return render_template('editarUsuario.html', usuario=usuario)


@app.route('/saveEditarUsuario',methods=['POST'])
@login_required
def saveeditarUsuario():
	id = int(request.form.get('id'))
	nome_form = request.form.get('nome')
	email_form = request.form.get('email')
	endereco_form = request.form.get('endereco')
	cidade_form = request.form.get('cidade')
	estado_form = request.form.get('estado')
	cep_form = request.form.get('cep')
	tipoUsuario_form = request.form.get('tipoUsuario')

	usuarios = UsuarioModel.query.filter_by(id=id).first()

	usuarios.nome = nome_form
	usuarios.email = email_form
	usuarios.endereco = endereco_form
	usuarios.cidade = cidade_form
	usuarios.estado = estado_form
	usuarios.cep = cep_form
	usuarios.tipoUsuario = tipoUsuario_form

	db.session.commit()

	usuarios = UsuarioModel.query.all()
	return render_template('listarUsuarios.html', usuarios=usuarios)
