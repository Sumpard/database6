import json
from app import app, db
from flask import render_template, redirect, jsonify, request

from util.result import Result
from entity.user import User


@app.route('/api/auth/register', methods=['POST', 'GET'])
def register():
    app.logger.info(request.json)
    username = request.json.get('username')
    password = request.json.get('password')
    name = request.json.get("name")
    phone = request.json.get('phone')
    email = request.json.get('email')
    address = request.json.get('address')

    if username and password:
        # username_exists = db.session.query(User).filter(User.uname == username).first()
        username_exists = False
        if username_exists:
            return jsonify(Result.fail('用户名已经存在'))

        user = User(uname=username, pwd=password, name=name, address=address, phone=phone, email=email)
        app.logger.info(user)
        db.session.add(user)
        db.session.commit()
        return jsonify(Result.success('注册成功'))

    else:
        return jsonify(Result.fail('输入信息不完整'))


@app.route('/api/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    if username:
        username_exists = db.session.query(User.user_pswd).filter(User.user_id == username).first()

        if username_exists:
            password_one = db.session.query(User.user_pswd).filter(User.user_id == username).first()
        if password in password_one:
            return redirect('/index')
        else:
            print('111')
            return render_template('login.html', msg='用户名或密码输入错误')

    else:
        print('222')
        return render_template('login.html', msg='用户名或密码输入错误')
