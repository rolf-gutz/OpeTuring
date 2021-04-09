
from flask import Flask,render_template,redirect,request,url_for,flash
from app import app, db,login_manager
from app.models.UsuarioModel import UsuarioModel
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def current_user(id):
    return UsuarioModel.query.get(id)

@app.route('/')
@app.route('/login',methods =["GET","POST"])
def login():
	if request.method =="POST":
		email = request.form['email']
		password = request.form['password']
		
		usuario = UsuarioModel.query.filter_by(email=email).first()

		if not usuario:
			flash("Credênciais incorretas")
			return redirect(url_for("login"))

		if not check_password_hash(usuario.password, password):
			flash("Senha  incorretas")
			return redirect(url_for("login"))

		login_user(usuario)
		return redirect(url_for('listagem'))
	
	return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("login.html")

