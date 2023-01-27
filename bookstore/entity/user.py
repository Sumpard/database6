from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean

from bookstore.application import db


class User(db.Model, UserMixin):  # type: ignore
    __tablename__ = 'user'
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    uname = Column(String(64), nullable=False, unique=True, index=True)  # 用户名
    pwd = Column(String(256), nullable=False)  # 密码，数据库存的是加密后的
    name = Column(String(64), default='')  # 姓名
    phone = Column(String(64), default='')  # 电话号码
    email = Column(String(64), default='')  # 邮箱
    address = Column(String(255), default='')  # 住址，后面偷懒直接拿来用了
    is_vip = Column(Boolean, default=False)  # 没用到
    is_valid = Column(Boolean, default=True)  # 没用到

    def __repr__(self):
        return f'<User {self.id} {self.uname}>'
