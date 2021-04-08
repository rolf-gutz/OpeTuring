from app import db
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user

class ProdutoModel(db.Model,UserMixin):
    __tablename__ = 'produto'

    idProduto = db.Column(db.Integer, primary_key=True)
    notaFiscal = db.Column(db.Integer,nullable = False)
    cnpj = db.Column(db.Integer,nullable = False)
    razaoSocial = db.Column(db.String(250),nullable=False)
    nome = db.Column(db.String(150),nullable=False)
    dataEntrada = db.Column(db.DateTime)
    saldo = db.Column(db.Float)
    prazoPagamento = db.Column(db.Integer)
    valorKg = db.Column(db.Float)
    caixa = db.Column(db.Float)
    sacos = db.Column(db.Integer)
    kg = db.Column(db.Float)


    def __init__(self,
                     notaFiscal,cnpj,razaoSocial,nome,dataEntrada,saldo,
                     prazoPagamento,valorKg,
                     caixa,sacos,kg):

        self.nome = nome
        self.email = email
        self.password = password
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.tipoUsuario = tipoUsuario

    def __repr__(self):
        return '<ProdutoModel %r>' % self.nome