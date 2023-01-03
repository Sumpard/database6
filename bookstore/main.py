import controller.login
from app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()  # 创建表
        app.run(debug=True)
