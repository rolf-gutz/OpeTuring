from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db, login_manager
from app.models.ProdutoModel import ProdutoModel
from app.models.Fornecedor import Fornecedor
from app.controllers.login.login import requires_roles
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import locale



@app.route('/cadastrarProduto')
# @requires_roles('Administrador')
# @login_required
def cadastrarProduto():
    fornecedores = Fornecedor.query.all()
    return render_template('produtos/cadastroProduto.html',fornecedores = fornecedores)

@app.route('/salvar_produto',methods=['POST'])
# @login_required
def salvar_produto():
    nome_form = request.form.get('nome')
    valor_form = request.form.get('valor')
    kg_form = request.form.get('kg')
    id_fornecedor_form = request.form.get('id_fornecedor') 
    
    produto = ProdutoModel(nome_form,valor_form,kg_form,id_fornecedor_form)
    if not CheckFormulario(produto):
        result = {'success': False }
        return result
    else:
        nome = request.form.get('nome')
        valor = float(request.form.get('valor'))
        kg = float(request.form.get('kg'))
        id_fornecedor = request.form.get('id_fornecedor') 

        db.session.add(produto)
        db.session.commit()
        result = {'success': True}
        return result  
    

def CheckFormulario(produto):
    if produto.nome == '' or produto.valor == '' or produto.kg == '' or produto.id_fornecedor == '':
        return  False
    else:
        return  True
    

 

    
# @app.route('/listarProdutos/<int:page>',methods=['POST'],defaults={'page':1})
@app.route('/listarProdutos')
@app.route('/listarProdutos/<int:page>')
# @login_required
def listarProdutos(page=1):
    produtos = produtosPagined(page)
    return render_template('produtos/listarProdutos.html', produtos=produtos)


@app.route('/deletarProduto/<int:id>')
# @login_required
def deletarProduto(id=0):
    produto = ProdutoModel.query.filter_by(idProduto=id).first()

    protudoconvertido  = ProdutoModel(produto.idProduto,produto.nome, ConverterMoeda(produto.valor),ConverterMoeda(produto.kg),produto.id_fornecedor) 

    fornecedores = Fornecedor.query.all()
    return render_template('produtos/deletarProduto.html', produto=protudoconvertido, fornecedores = fornecedores)


@app.route('/saveDeleteProduto',methods=['POST'])
# @login_required
def saveDeleteProduto():
    id = int(request.form.get('idProduto'))

    produto = ProdutoModel.query.filter_by(idProduto=id).first()

    db.session.delete(produto)
    db.session.commit()
	
    produtosArray = produtosPagined()
    return render_template('produtos/listarProdutos.html', produtos = produtosArray)


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

    produto = ProdutoModel.query.filter_by(idProduto=id).first()
  
    produto.nome = nome
    produto.valor = valor
    produto.kg = kg
    produto.id_fornecedor = id_fornecedor

    db.session.commit()

    produtosArray = produtosPagined()
    return render_template('produtos/listarProdutos.html', produtos = produtosArray)


def produtosPagined (page=1):
    page = page
    produtosArray = []
    produtos = ProdutoModel.query.paginate(page , 15, False)
    if (produtos.pages > 0): 
        produtosArray = ProdutosArray(produtos)
    else:
        return produtos
    return produtosArray

    
def ProdutosArray (produtos):
    produtosResult = {'has_next': produtos.has_next,
                    'has_prev':produtos.has_prev,
                    'items': [],
                    'next_num' : produtos.next_num,
                    'page': produtos.page,
                    'pages':produtos.pages,
                    'per_page':produtos.per_page,
                    'prev_num': produtos.prev_num
                    }
    itens = len(produtos.items)
    for x in range(itens):
        produtoJson = {'idProduto': produtos.items[x].idProduto,
                        'nome': produtos.items[x].nome,
                        'valor': ConverterMoeda(produtos.items[x].valor),
                        'kg': ConverterQuilos(produtos.items[x].kg) 
                        }
        produtosResult['items'].append(produtoJson)
    
    return produtosResult

def ConverterMoeda(my_value):
    moeda = 'R$ '
    a = '{:,.2f}'.format(float(my_value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return moeda + c.replace('v','.')

    
def ConverterQuilos(my_value):
    a = '{:,.0f}'.format(float(my_value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return c.replace('v','.')