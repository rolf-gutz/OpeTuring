from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db, login_manager
from app.models.PessoaModel import Pessoa
from app.models.UsuarioModel import UsuarioModel
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash



# AUTENTICAÇÃO
# *********************************************************

@login_manager.user_loader
def current_user(id):
    return UsuarioModel.query.get(id)

@app.route('/')
@app.route('/login',methods =["GET","POST"])
def login():
	if request.method =="POST":
		email = request.form['email']
		password = request.form['password']
		
		usuario = UsuarioModel.query.filter_by(email=email).first()

		if not usuario:
			flash("Credênciais incorretas")
			return redirect(url_for("login"))

		if not check_password_hash(usuario.password, password):
			flash("Senha  incorretas")
			return redirect(url_for("login"))

		login_user(usuario)
		return redirect(url_for('listagem'))
	
	return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("login.html")

# *********************************************************



#  USUARIO
# *********************************************************

@app.route('/cadastrarUsuario')
@login_required
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
def listarUsuarios():
	usuarios = UsuarioModel.query.all()
	return render_template('listarUsuarios.html', usuarios=usuarios)


@app.route('/deletarUsuario/<int:id>')
@login_required
def deletarUsuario(id=0):
	usuario = usuarios = UsuarioModel.query.filter_by(id=id).first()

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

# *********************************************************


@app.route('/listagem')
@login_required
def listagem():
	pessoas = Pessoa.query.all()
	return render_template('listagem.html', pessoas=pessoas, ordem='id')

@app.route('/selecao/<int:id>')
@login_required
def selecao(id=0):
	pessoas = Pessoa.query.filter_by(id=id).all()
	return render_template('listagem.html',pessoas=pessoas,ordem='id')

@app.route('/ordenacao/<campo>/<ordem_anterior>')
@login_required
def ordenacao(campo='id', ordem_anterior=''):
	if campo =='id':
		if ordem_anterior == campo:
			pessoas = Pessoa.query.order_by(Pessoa.id.desc()).all()
		else:
			pessoas = Pessoa.query.order_by(Pessoa.id).all()
	elif campo == 'nome':
		if ordem_anterior == campo:
			pessoas = Pessoa.query.order_by(Pessoa.nome.desc()).all()
		else:
			pessoas = Pessoa.query.order_by(Pessoa.nome).all()
	elif campo == 'idade':
		if ordem_anterior == campo:
			pessoas = Pessoa.query.order_by(Pessoa.idade.desc()).all()
		else:
			pessoas = Pessoa.query.order_by(Pessoa.idade).all()
	elif campo == 'sexo':
		if ordem_anterior == campo:
			pessoas = Pessoa.query.order_by(Pessoa.sexo.desc()).all()
		else:
			pessoas = Pessoa.query.order_by(Pessoa.sexo).all()
	elif campo == 'salario':
		if ordem_anterior == campo:
			pessoas = Pessoa.query.order_by(Pessoa.salario.desc()).all()
		else:
			pessoas = Pessoa.query.order_by(Pessoa.salario).all()
	else:
		pessoas = Pessoa.query.order_by(Pessoa.id).all()

	return render_template('listagem.html',pessoas=pessoas,ordem=campo)

@app.route('/consulta',methods=['POST'])
@login_required
def consulta():
	consulta = '%'+request.form.get('consulta')+'%'
	campo = request.form.get('campo')
	
	if campo == 'nome':
		pessoas = Pessoa.query.filter(Pessoa.nome.like(consulta)).all()
	elif campo == 'idade':
		pessoas = Pessoa.query.filter(Pessoa.idade.like(consulta)).all()
	elif campo == 'sexo':
		pessoas = Pessoa.query.filter(Pessoa.sexo.like(consulta)).all()
	elif campo == 'salario':
		pessoas = Pessoa.query.filter(Pessoa.salario.like(consulta)).all()
	else:
		pessoas = Pessoa.query.all()
	
	return render_template('listagem.html',pessoas = pessoas,ordem ='id')


@app.route('/insercao')
@login_required
def insercao():
	return render_template('insercao.html')

@app.route('/salvar_insercao',methods=['POST'])
def salvar_insercao():
	nome = request.form.get('nome')
	idade = int(request.form.get('idade'))
	sexo = request.form.get('sexo')
	salario = float(request.form.get('salario'))

	pessoa = Pessoa(nome,idade,sexo,salario)

	db.session.add(pessoa)
	db.session.commit()

	pessoas = Pessoa.query.all()
	return render_template('listagem.html',pessoas=  pessoas, ordem='id')

@app.route('/edicao/<int:id>')
@login_required
def edicao(id=0):
	pessoa = Pessoa.query.filter_by(id =id).first()
	return render_template('edicao.html',pessoa = pessoa)


@app.route('/salvar_edicao',methods=['POST'])
@login_required
def salvar_edicao():
	Id = int(request.form.get('id'))
	Nome = request.form.get('nome')
	Idade = int(request.form.get('idade'))
	Sexo = request.form.get('sexo')
	Salario = float(request.form.get('salario'))

	pessoa = Pessoa.query.filter_by(id=Id).first()

	pessoa.nome = Nome
	pessoa.idade = Idade
	pessoa.sexo = Sexo
	pessoa.salario = Salario

	db.session.commit()

	pessoas = Pessoa.query.all()
	return render_template('listagem.html',pessoas=  pessoas, ordem='id')

@app.route('/delecao/<int:id>')
@login_required
def delecao(id=0):
	pessoa = Pessoa.query.filter_by(id=id).first()
	return render_template('delecao.html', pessoa=pessoa)

@app.route('/salvar_delecao', methods=['POST'])
@login_required
def salvar_delecao():
	Id = int(request.form.get('id'))

	pessoa = Pessoa.query.filter_by(id=Id).first()

	db.session.delete(pessoa)
	db.session.commit()

	pessoas = Pessoa.query.all()
	return render_template('listagem.html',pessoas= pessoas, ordem='id')
	

@app.route('/graficos')
@login_required
def graficos():
	pessoasM = Pessoa.query.filter_by(sexo='M').all()
	pessoasF = Pessoa.query.filter_by(sexo='F').all()
	
	salarioM = 0
	for m in pessoasM:
		salarioM += m.salario
	if len(pessoasM) > 0:
		salarioM = salarioM / len(pessoasM)

	salarioF = 0
	for f in pessoasF:
		salarioF += f.salario
	if len(pessoasF) > 0:
		salarioF = salarioF / len(pessoasF)
		
	IdadeM = 0
	for m in pessoasM:
			IdadeM += m.idade
	if len(pessoasM) > 0:
			IdadeM = IdadeM / len(pessoasM)

	IdadeF = 0
	for f in pessoasF:
		IdadeF += f.idade
	if len(pessoasF) > 0:
		IdadeF = IdadeF / len(pessoasF)
			
	return render_template('graficos.html',
							salarioM=salarioM,salarioF=salarioF,idadeM=IdadeM,idadeF=IdadeF)


	