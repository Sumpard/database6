import logging
import traceback

from flask import Flask, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.scoping import scoped_session

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

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


@app.after_request
def after(resp):
    '''
    被after_request钩子函数装饰过的视图函数
    ，会在请求得到响应后返回给用户前调用，也就是说，这个时候，
    请求已经被app.route装饰的函数响应过了，已经形成了response，这个时
    候我们可以对response进行一些列操作，我们在这个钩子函数中添加headers，所有的url跨域请求都会允许！！！
    '''
    resp = make_response(resp)
    # resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    # resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp