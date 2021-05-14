from app.models.Pedido import Pedido
from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db, login_manager
from app.models.ProdutoModel import ProdutoModel
from app.models.ItensPedido import Itens_Pedido
from app.controllers.login.login import requires_roles 
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
import json 


@app.route('/selecionarProdutos')
@app.route('/selecionarProdutos/<int:page>')
# @login_required
def selecionarProdutos(page=1):
    produtos = produtosPagined(page)
    return render_template('pedidos/selecionarProdutos.html', produtos=produtos)     


@app.route('/pedido/addPedido/', methods=['POST'])
@login_required
def addPedido():    
    pedido = Pedido(0,0,None,None,0,'',current_user.id_empresa,current_user.id) 
    produtosLista = request.form['lista']
    jsonresult = json.loads(produtosLista)
    
    db.session.add(pedido)
    db.session.commit()        

    valor_total = 0
    for p in jsonresult:
        itens = Itens_Pedido(pedido.id_pedido,p['idProduto'],float(p['valorProduto']),float(p['quantity']))
                
        valor_total += itens.valorProduto()
        db.session.add(itens)
        db.session.commit()
    
    pedido.valor =  valor_total
    
    db.session.commit()   

    return render_template('detalhesPedido.html',id_pedido = pedido.id_pedido)

def produtosPagined (page=1):
    page = page
    produtos = ProdutoModel.query.paginate(page , 15, False)
    return produtos