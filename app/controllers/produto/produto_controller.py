from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db, login_manager
from app.models.PessoaModel import Pessoa
from app.models.UsuarioModel import UsuarioModel
from app.models.ProdutoModel import ProdutoModel
from app.models.Fornecedor import Fornecedor
from app.controllers.login.login import requires_roles
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date



@app.route('/cadastrarProduto')
# @requires_roles('Administrador')
# @login_required
def cadastrarProduto():
    fornecedores = Fornecedor.query.all()
    return render_template('produtos/cadastroProduto.html',fornecedores = fornecedores)

@app.route('/salvar_produto',methods=['POST'])
# @login_required
def salvar_produto():
    nome = request.form.get('nome')
    valor = float(request.form.get('valor'))
    kg = float(request.form.get('kg'))
    id_fornecedor = request.form.get('id_fornecedor')
    
    # dataEntrada = datetime.strptime(dataEntrada, "%Y-%m-%d").date()

    produto = ProdutoModel(nome,valor,kg,id_fornecedor)

    db.session.add(produto)
    db.session.commit()

    produtos = ProdutoModel.query.all()
    return render_template('produtos/listarProdutos.html', produtos = produtos)
    
    
@app.route('/listarProdutos')
# @login_required
def listarProdutos():
	produtos = ProdutoModel.query.all()
	return render_template('produtos/listarProdutos.html', produtos=produtos)



@app.route('/deletarProduto/<int:id>')
# @login_required
def deletarProduto(id=0):
	produto = ProdutoModel.query.filter_by(idProduto=id).first()
	return render_template('produtos/deletarProduto.html', produto=produto)


@app.route('/saveDeleteProduto',methods=['POST'])
# @login_required
def saveDeleteProduto():
	id = int(request.form.get('idProduto'))

	produto = ProdutoModel.query.filter_by(idProduto=id).first()

	db.session.delete(produto)
	db.session.commit()
	
	produtos = ProdutoModel.query.all()
	return render_template('produtos/listarProdutos.html', produtos=produtos)


@app.route('/editarProduto/<int:id>')
# @login_required
def editarProduto(id=0):
	produto = ProdutoModel.query.filter_by(idProduto=id).first()
	return render_template('produtos/editarProduto.html', produto=produto)


@app.route('/saveEditarProduto',methods=['POST'])
# @login_required
def saveEditarProduto():
    id = int(request.form.get('idProduto'))
    notaFiscal = int(request.form.get('notaFiscal'))
    cnpj = int(request.form.get('cnpj'))
    razaoSocial = request.form.get('razaoSocial')
    nome = request.form.get('nome')
    dataEntrada = request.form.get('dataentrada')
    saldo = float(request.form.get('saldo'))
    prazoPagamento = int(request.form.get('prazopagamento'))
    valorkg = float(request.form.get('valorkg'))
    caixa = float(request.form.get('caixa'))
    sacos = int(request.form.get('sacos'))
    kg = float(request.form.get('kg'))

    dataEntrada = datetime.strptime(dataEntrada, "%Y-%m-%d").date()

    produto = ProdutoModel.query.filter_by(idProduto=id).first()

    produto.notaFiscal = notaFiscal
    produto.cnpj = cnpj
    produto.razaoSocial = razaoSocial
    produto.nome = nome
    produto.dataEntrada = dataEntrada
    produto.saldo = saldo
    produto.prazoPagamento = prazoPagamento
    produto.valorkg = valorkg
    produto.caixa = caixa
    produto.sacos = sacos
    produto.kg = kg

    db.session.commit()

    produtos = ProdutoModel.query.all()
    return render_template('produtos/listarProdutos.html', produtos=produtos)