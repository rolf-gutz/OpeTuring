from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db, login_manager
from app.models.PessoaModel import Pessoa
from app.models.UsuarioModel import UsuarioModel
from app.models.ProdutoModel import ProdutoModel
from app.controllers.login.login import requires_roles 
from app.models.Empresa import Empresa
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
import json 


@app.route('/selecionarProdutos')
# @login_required
def selecionarProdutos():
    produtos = ProdutoModel.query.all()
    return render_template('pedidos/selecionarProdutos.html', produtos=produtos)     
	# return render_template('pedidos/adicionarCarrinho.html')       
    # return redirect(url_for('listarProdutos')) 




@app.route('/pedido/addPedido/', methods=['POST'])
# @login_required
def addPedido():
    array_of_objects = request.form['lista']
    jsonresult = json.loads(array_of_objects)
   
    pedido =  {'idPedido': 1}
    return pedido

