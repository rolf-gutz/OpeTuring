
from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db,login_manager
from app.models.UsuarioModel import UsuarioModel
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


# @login_manager.user_loader
# def current_user(id):
#     return UsuarioModel.query.get(id)

@app.route('/')
@app.route('/login',methods =["GET","POST"])
def login():
	if request.method =="POST":
		email = request.form['email']
		password = request.form['password']
		
		usuario = UsuarioModel.query.filter_by(email=email).first()

		if not usuario:
			flash("Credenciais incorretas")
			return redirect(url_for("login"))

		if not check_password_hash(usuario.password, password):
			flash("Senha incorreta")
			return redirect(url_for("login"))

		login_user(usuario)
		return redirect(url_for('listagem'))

		
	return render_template('login/login.html')

@login_manager.user_loader
def load_user(id):  
	usuario = UsuarioModel.query.filter_by(id=id).first()
	return usuario

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("login.html")


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.tipoUsuario not in roles:
                # Redirect the user to an unauthorized notice!
                return render_template('naoautorizado.html')
            return f(*args, **kwargs)
        return wrapped
    return wrapper