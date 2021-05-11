from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db, login_manager
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

    produtos = produtosPagined(page=1)
    return render_template('produtos/listarProdutos.html', produtos=produtos)
    
    
# @app.route('/listarProdutos/<int:page>',methods=['POST'],defaults={'page':1})
@app.route('/listarProdutos/1')
@app.route('/listarProdutos/<int:page>')
# @login_required
def listarProdutos(page=1):
    produtos = produtosPagined(page)
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
	
    # produtos = ProdutoModel.query.all()
    # produtosArray = modelArray(produtos)
    return url_for('/listarProdutos/')


@app.route('/editarProduto/<int:id>')
# @login_required
def editarProduto(id=0):
    produto = ProdutoModel.query.filter_by(idProduto=id).first()
    fornecedores = Fornecedor.query.all()
    return render_template('produtos/editarProduto.html', produto=produto, fornecedores = fornecedores)

@app.route('/saveEditarProduto',methods=['POST'])
# @login_required
def saveEditarProduto():
    id = int(request.form.get('idProduto'))
    nome = request.form.get('nome')
    valor = float(request.form.get('valor'))
    kg = float(request.form.get('kg'))
    id_fornecedor = request.form.get('id_fornecedor')

    # dataEntrada = datetime.strptime(dataEntrada, "%Y-%m-%d").date()

    produto = ProdutoModel.query.filter_by(idProduto=id).first()
  
    produto.nome = nome
    produto.valor = valor
    produto.kg = kg
    produto.id_fornecedor = id_fornecedor

    db.session.commit()

    produtos = ProdutoModel.query.all()
    produtosArray = modelArray(produtos)
    return render_template('produtos/listarProdutos.html', produtos = produtosArray)
    
def conversorMoeda (valor = 0 , moeda='R$'):
        return f'{moeda}{valor:.2f}'.replace('.',',')


def modelArray (produtos):
    produtosArray  = []
    for x in produtos:
        produtoJson = {'idProduto': x.idProduto,
                    'nome':x.nome,
                    'valor': conversorMoeda(x.valor),
                    'kg': x.kg ,
                    'Pagination' : x.Pagination              
            }
        produtosArray.append(produtoJson)
    
    return produtosArray

def produtosPagined (page=1):
    page = page
    produtos = ProdutoModel.query.paginate(page , 15, False)
    return produtos