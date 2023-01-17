import traceback
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'root'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/bookstore'
# 协议：mysql+pymysql
# 用户名：root
# 密码：123456
# IP地址：localhost
# 端口：3306
# 数据库名：test #这里的数据库需要提前建好
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


@app.errorhandler(Exception)
def _error_handler(error: Exception):
    app.logger.error(error)
    app.logger.error(traceback.format_exc())