from os.path import join, dirname, realpath
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/files/')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f106a85651d73990e22af513b9dbfa24'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'front_page'
login_manager.login_message_category = 'info'
login_manager.login_message = u"Пожалуйста, войдите в учётную запись"


from FarmCalculator import routes
