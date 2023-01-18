from pathlib import Path
import sys
import sqlalchemy as sa
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative
from entity.user import User
from entity.comments import Comments
from entity.book import Book
import query
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
        query.Search_union('耶鲁大学','','出版','')
        query.Search_or('耶鲁大学','吴','出版公司','这本书')
        app.run(debug=True)
