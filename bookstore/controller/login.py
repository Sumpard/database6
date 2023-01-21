import base64
from datetime import timedelta
from typing import Optional

from flask import request
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from bookstore.application import app, db
from bookstore.entity.user import User
from bookstore.util.result import Result
from bookstore.util.rsa_decrypt import rsa_decrypt

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(id):
    app.logger.info(f"load user: {id} {User.query.get(int(id))}")
    return User.query.get(int(id))


@app.route('/api/auth/register', methods=['POST'])
def register():
    data: dict = request.json or {}
    app.logger.info(data)
    username = data.get('username')
    password = data.get('password')
    name = data.get("name")
    phone = data.get('phone')
    email = data.get('email')
    address = data.get('address')

    if not (username and password):
        return Result.fail('输入信息不完整')

    username_exists = db.session.query(User).filter(User.uname == username).first()
    if username_exists:
        return Result.fail('用户名已经存在')

    user = User(uname=username, pwd=password, name=name, address=address, phone=phone, email=email)
    db.session.add(user)
    db.session.commit()
    return Result.success('注册成功')


@app.route('/api/auth/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        # return Result.fail("用户已登录")
        logout_user()

    data: dict = request.json or {}
    username = data.get('username')
    password = data.get('password')

    if not (username and password):
        return Result.fail('缺少用户名或密码')

    user: Optional[User] = db.session.query(User).filter(User.uname == username).first()

    if not user:
        return Result.fail("用户不存在")

    password = rsa_decrypt(base64.b64decode(password))
    user_pwd = rsa_decrypt(base64.b64decode(user.pwd))

    if user_pwd != password:
        app.logger.info("Wrong password. Expected %s, got %s.", user_pwd, password)
        return Result.fail("密码错误")

    login_user(user, remember=True, duration=timedelta(7))
    # login_user(user)

    return Result.success("成功登录", user)


@app.route('/api/auth/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return Result.success("成功登出")


@app.route('/api/auth', methods=['GET'])
@login_required
def authentication():
    return Result.success("身份认证成功")
