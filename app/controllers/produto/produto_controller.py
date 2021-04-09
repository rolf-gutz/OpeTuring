from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db, login_manager
from app.models.PessoaModel import Pessoa
from app.models.UsuarioModel import UsuarioModel
from app.models.ProdutoModel import ProdutoModel
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date



@app.route('/cadastrarProduto')
@login_required
def cadastrarProduto():
	return render_template('cadastroProduto.html')

@app.route('/salvar_produto',methods=['POST'])
@login_required
def salvar_produto():
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


    produto = ProdutoModel(notaFiscal,cnpj,razaoSocial,nome,dataEntrada,saldo,
                            prazoPagamento,valorkg,
                            caixa,sacos,kg)

    db.session.add(produto)
    db.session.commit()

    produtos = ProdutoModel.query.all()
    return render_template('listarProdutos.html', produtos= produtos)
    
    
@app.route('/listarProdutos')
@login_required
def listarProdutos():
	produtos = ProdutoModel.query.all()
	return render_template('listarProdutos.html', produtos=produtos)
