from app import db
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from datetime import datetime, date

class ProdutoModel(db.Model,UserMixin):
    __tablename__ = 'produto'

    idProduto = db.Column(db.Integer, primary_key=True)
    notaFiscal = db.Column(db.Integer,nullable = False)
    cnpj = db.Column(db.Integer,nullable = False)
    razaoSocial = db.Column(db.String(250),nullable=False)
    nome = db.Column(db.String(150),nullable=False)
    dataEntrada = db.Column(db.Date, default = date.today())
    # cumpoDesconto = db.Column(db.String(50))
    # prazoPagamento = db.Column(db.Integer)
    valorkg = db.Column(db.Float)
    # sacos = db.Column(db.Integer)
    kg = db.Column(db.Float)


    def __init__(self,
                     notaFiscal,cnpj,razaoSocial,nome,dataEntrada,saldo,
                     prazoPagamento,valorkg,
                     caixa,sacos,kg):

        self.notaFiscal = notaFiscal
        self.cnpj = cnpj
        self.razaoSocial = razaoSocial
        self.nome = nome
        self.dataEntrada = dataEntrada
        self.saldo = saldo
        self.prazoPagamento = prazoPagamento
        self.valorkg = valorkg
        self.caixa = caixa
        self.sacos = sacos
        self.kg = kg

    def __repr__(self):
        return '<ProdutoModel %r>' % self.nome