from application import db
from data import Users
#import sys


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    uname = db.Column(db.String(64), nullable=False)
    pwd = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(64), default='')
    phone = db.Column(db.String(64), default='')
    email = db.Column(db.String(64), default='')
    address = db.Column(db.String(255), default='')
    is_vip = db.Column(db.Boolean, default=False)
    is_valid = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.id} {self.uname}>'

    def add_data(t):
        for i in range(t):
            info = Users(i)
            user=User(id=info[0], uname=info[1], pwd=info[2],name=info[3],
                phone=info[4], email=info[5], address=info[6],  is_vip=info[7], is_valid=info[8])
            db.session.add(user)
            db.session.commit()