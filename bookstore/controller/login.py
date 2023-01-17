import base64
from typing import Optional

from application import app, db
from entity.user import User
from flask import request
from util.result import Result
from util.rsa_decrypt import rsa_decrypt


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

    app.logger.info(isinstance(user, db.Model))

    return Result.success("成功登录", user)
