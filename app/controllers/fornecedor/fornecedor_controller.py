from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db, login_manager
from app.models.PessoaModel import Pessoa
from app.models.UsuarioModel import UsuarioModel
from app.models.ProdutoModel import ProdutoModel
from app.models.Fornecedor import Fornecedor
from app.controllers.login.login import requires_roles 
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import re


@app.route('/cadastrarFornecedor')
# @login_required
def cadastrarFornecedor():
    return render_template('fornecedor/cadastroFornecedor.html')


@app.route('/salvarFornecedor',methods=['POST'])
# @login_required
def salvarFornecedor():
    cnpj = int(re.sub("[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]+","",request.form.get('cnpj')))
    razao_social = request.form.get('razao_social')
    nome = request.form.get('nome')
                        
    fornecedor = Fornecedor(cnpj,razao_social,nome)

    db.session.add(fornecedor)
    db.session.commit()

    fornecedores = Fornecedor.query.all()
    return render_template('fornecedor/listarFornecedor.html', fornecedores = fornecedores)
    
@app.route('/listarFornecedor')
# @login_required
# @requires_roles('Cliente')
def listarFornecedor():
	fornecedores = Fornecedor.query.all()
	return render_template('fornecedor/listarFornecedor.html', fornecedores = fornecedores)


@app.route('/deletarFornecedor/<int:id>')
# @login_required
def deletarFornecedor(id=0):
	fornecedor = Fornecedor.query.filter_by(id_fornecedor=id).first()
	return render_template('fornecedor/deletarFornecedor.html', fornecedor = fornecedor)

    
# @app.route('/saveDeletarFornecedor',methods=['POST'])
# # @login_required
# def saveDeletarFornecedor():
# 	id = int(request.form.get('id_empresa'))
# 	fornecedor = Fornecedor.query.filter_by(id_empresa=id).first()
	
# 	db.session.delete(fornecedor)
# 	db.session.commit()
	
# 	fornecedor = Fornecedor.query.all()
# 	return render_template('fornecedor/listarEmpresa.html',  fornecedor = fornecedor)


# @app.route('/editarFornecedor/<int:id>')
# # @login_required
# def editarFornecedor(id=0):
# 	fornecedor =  Fornecedor.query.filter_by(id_empresa=id).first()
# 	return render_template('fornecedor/editarEmpresa.html', fornecedor = fornecedor)


# @app.route('/saveEditarFornecedor',methods=['POST'])
# # @login_required
# def saveeditarFornecedor():
# 	id = int(request.form.get('id_empresa'))
# 	razao_social = request.form.get('razao_social')
# 	text2 = re.sub("[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]+","",request.form.get('cnpj'))
# 	cnpj = int(text2)
# 	nome = request.form.get('nome')
# 	endereco = request.form.get('endereco')
# 	cidade = request.form.get('cidade')
# 	estado = request.form.get('estado')
# 	cep = request.form.get('cep')

# 	fornecedor = Fornecedor.query.filter_by(id_empresa=id).first()

# 	empresa.razao_social =razao_social
# 	empresa.nome = nome
# 	empresa.cnpj = cnpj
# 	empresa.endereco = endereco
# 	empresa.cidade = cidade
# 	empresa.estado = estado
# 	empresa.cep = cep

# 	db.session.commit()

# 	fornecedores = Fornecedor.query.all()
# 	return render_template('fornecedor/listarEmpresa.html', fornecedores = fornecedores)

