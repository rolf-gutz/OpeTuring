from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager, UserMixin, login_required,login_user, logout_user


app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app.controllers import default
from app.controllers.login import login
from app.controllers.usuario import usuario_controller
