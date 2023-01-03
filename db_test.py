from flask import Flask, render_template, redirect, url_for, jsonify, request,session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/test'
# 协议：mysql+pymysql
# 用户名：root
# 密码：123456
# IP地址：localhost
# 端口：3306
# 数据库名：test #这里的数据库需要提前建好
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


@app.route('/')
def db_test():
    dict_show = {}  # 定义字典用于数据展示
    # 反射数据库中已存在的表，并获取所有存在的表对象。
    db.reflect()
    # 获取所有表名
    all_table = {
        table_obj.name: table_obj for table_obj in db.get_tables_for_bind()}
    # 获取demo表的所有数据
    all_data = db.session.query(all_table['user_data'])
    for data in all_data:
        print(data)  # 查看数据
        dict_show[data[0]] = [data[1], data[2]]
    # 将字典转换成json数据
    return jsonify(dict_show)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form.get('username')
    password = request.form.get('password')

    if username:
        username_exists = db.session.query(User.user_pswd).filter(User.user_id == username).first()
       
        if username_exists:
            password_one = db.session.query(User.user_pswd).filter(
            User.user_id == username).first()  
        if password in password_one:
            return redirect('/index')
        else:
            print('111')
            return render_template('login.html',msg='用户名或密码输入错误')
    
    else:
        print('222')
        return render_template('login.html',msg='用户名或密码输入错误')


@app.route('/index')
def index():
    print('chenggong')
    return "登陆成功！"


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    username = request.form.get('username')
    password = request.form.get('password')
    address = request.form.get('address')
    tel = request.form.get('tel')

    if username and password and address and tel:
        username_exists = db.session.query(User.user_pswd).filter(User.user_id == username).first()
       
        if username_exists:
            return render_template('register.html',msg='用户名已经存在')
        user=User(user_id=username,user_pswd=password,user_address=address,user_tel=tel,is_vip="否",is_valid="否")
        db.session.add(user)
        db.session.commit()
        return render_template('register.html',msg='注册成功')
    
    else:
        return render_template('register.html',msg='输入信息不完整')




# 新建表User
class User(db.Model):
    __tablename__ = 'user_data'
    user_id = db.Column(db.String(64), primary_key=True)
    user_pswd = db.Column(db.String(64), index=True)
    user_address = db.Column(db.String(255))
    user_tel = db.Column(db.String(64), unique=True)
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 外键
    is_vip=db.column(db.String(64))
    is_valid=db.column(db.String(64))
    def __repr__(self):
        return '<User %r>' % self.user_id


if __name__ == '__main__':
    with app.app_context():
        #db.create_all()  # 创建表
        app.run(debug=True)
