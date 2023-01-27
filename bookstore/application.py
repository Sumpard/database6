import logging
import traceback

from flask import Flask, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.scoping import scoped_session

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:*", "http://127.0.0.1:*"])

app.config['JSON_AS_ASCII'] = False
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
# app.config['SQLALCHEMY_ECHO'] = True
app.logger.setLevel(logging.INFO)
db = SQLAlchemy(app)
session: scoped_session = db.session


@app.errorhandler(Exception)
def _error_handler(error: Exception):
    app.logger.error(error)
    app.logger.error(traceback.format_exc())
    return "An Error Occurred", 500


from datetime import date, datetime

from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return JSONEncoder.default(self, obj)


app.json_encoder = CustomJSONEncoder
