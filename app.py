from flask import Flask

import accounts
import qa
from models import db, User

app = Flask(__name__, static_folder='medias')
app.config.from_object('conf.Config')

db.init_app(app)

# 注册蓝图
app.register_blueprint(accounts, url_prefix='/accounts')
app.register_blueprint(qa, url_prefix='/qa')