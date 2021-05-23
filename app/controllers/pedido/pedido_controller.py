from flask_migrate import current
from sqlalchemy.orm import query
from app.models.Pedido import Pedido
from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db, login_manager
from app.models.ProdutoModel import ProdutoModel
from app.models.ItensPedido import Itens_Pedido
from app.models.Empresa import Empresa
from app.models.UsuarioModel import UsuarioModel
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
    produtosPagina = ConvertePagina(produtos)
    return render_template('pedidos/selecionarProdutos.html', produtos=produtosPagina)     


@app.route('/pedido/addPedido/', methods=['POST'])
# @login_required
def addPedido():    
    pedido = Pedido(0,0,None,None,0,'',current_user.id_empresa,current_user.id) 
    produtosLista = request.form['lista']
    jsonresult = json.loads(produtosLista)
    
    db.session.add(pedido)
    db.session.commit()        

    valor_total = 0
    sobra = 0
    for p in jsonresult:
        produtoBanco = ProdutoModel.query.filter_by(idProduto = p['idProduto']).first()
        itens = Itens_Pedido(pedido.id_pedido,p['idProduto'],float(p['valorProduto']),float(p['quantity']))
        valor_total += itens.valorProduto()

        quilos = produtoBanco.kg 
        sobra = quilos - int(p['quantity'])
        produtoBanco.kg = sobra
        
        db.session.commit()

        db.session.add(itens)
        db.session.commit()


    pedido.valor =  valor_total
    
    db.session.commit()   

    itensPedido  = PedidoItensArray(pedido)
    return itensPedido 

@app.route('/listarPedidos/')
@app.route('/listarPedidos/<int:page>')
def listarPedidos(page=1):
    pedidos = PedidosPagined(page)
    return render_template('pedidos/listarPedidos.html', pedidoArray = pedidos)

@app.route('/detalhesPedido/<int:id>')
def detalhesPedido(id):
    pedido = Pedido.query.filter_by(id_pedido=id).first()
    itensPedido  = PedidoItensArray(pedido)
    return render_template('/pedidos/detalhesPedido.html',   itensPedido = itensPedido)

def produtosPagined (page=1):
    page = page
    produtos = ProdutoModel.query.filter(ProdutoModel.kg > 0).paginate(page,15,False)
    return produtos

def ConvertePagina(produtos):
    produtoResult = {'has_next': produtos.has_next,
                    'has_prev':produtos.has_prev,
                    'items': [],
                    'next_num' : produtos.next_num,
                    'page': produtos.page,
                    'pages':produtos.pages,
                    'per_page':produtos.per_page,
                    'prev_num': produtos.prev_num
                    }
    totalItens = len(produtos.items)
    for index in range(totalItens):
        produto = { 'idProduto' : produtos.items[index].idProduto,
                    'nome':produtos.items[index].nome,
                    'valorTela':ConverterMoeda(produtos.items[index].valor),
                    'valor':produtos.items[index].valor,
                    'kg':ConverterQuilos(produtos.items[index].kg),
                    'id_fornecedor':produtos.items[index].id_fornecedor
                   }

        produtoResult['items'].append(produto)
    
    return produtoResult


def Pedidosarray(pedido):
    pedidoResult = {'has_next': pedido.has_next,
                    'has_prev':pedido.has_prev,
                    'items': [],
                    'next_num' : pedido.next_num,
                    'page': pedido.page,
                    'pages':pedido.pages,
                    'per_page':pedido.per_page,
                    'prev_num': pedido.prev_num
                    }
    
    itens = len(pedido.items)
    for index in range(itens):
        empresa = Empresa.query.filter_by(id_empresa = pedido.items[index].id_empresa_funcionario).first()
        usuario = UsuarioModel.query.filter_by(id = pedido.items[index].id_funcionario).first()
        
        detalhesPedido =  { 'razaoSocial' :  empresa.razao_social,
                            'nomeUsuario' :usuario.nome,
                            'numeroPedido' : pedido.items[index].id_pedido,
                            'DatadoPedido' : pedido.items[index].dataPedido,
                            'ValorPedido' : ConverterMoeda(pedido.items[index].valor),
                            'StatusdePagamento' : StatusDePagamento(pedido.items[index].statusPagamento)
                        }
        
        pedidoResult['items'].append(detalhesPedido)
    
    return pedidoResult

def PedidoItensArray(pedido):
    empresa = Empresa.query.filter_by(id_empresa = pedido.id_empresa_funcionario).first()
    itens = Itens_Pedido.query.filter_by(id_pedido = pedido.id_pedido).all()
    produtosDoPedido = []

    for x in itens:        
        produto  = ProdutoModel.query.filter_by(idProduto = x.id_produto).first()
        if x.id_produto == produto.idProduto:
            itemNome = produto.nome       
            produtoValor = x.valor
            quantidade = x.kg 
            p = {'nome' : itemNome,
                'produtoValor': produtoValor ,
                'quantidade': quantidade
                 }
            produtosDoPedido.append(p)
            
    detalhesPedido = { 'razaoSocial' :  empresa.razao_social,
                    'numeroPedido' : pedido.id_pedido,
                    'DatadoPedido' : pedido.dataPedido,
                    'ValorTotalPedido' : pedido.valor,
                    'produtos' : produtosDoPedido
                    }
            
    return detalhesPedido   
    
def PedidosPagined (page=1):
    page = page
    pedidoArray = []
    pedido = Pedido.query.paginate(page , 15, False)
    if (pedido.pages > 0): 
        pedidoArray = Pedidosarray(pedido)
    else:
        return pedido
    return pedidoArray

def StatusDePagamento(status):
    if status  == False:
        return 'Em Aberto'
    elif status == True:
        return 'Pago'
    else:
        return 'Em Aberto'

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