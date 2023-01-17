from pathlib import Path
import sys
import sqlalchemy as sa
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative
from entity.user import User
from entity.comments import Comments
from entity.book import Book
sys.path.append(str(Path(__file__).parent.absolute()))

import controllers.login
from application import app, db

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()  # 创建表
        User.add_data(100)
        Comments.add_data(100)
        Book.add_data()
        app.run(debug=True)
