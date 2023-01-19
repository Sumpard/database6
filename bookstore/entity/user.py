from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

from bookstore.application import db


class User(db.Model):  # type: ignore
    __tablename__ = 'user'
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    uname = Column(String(64), nullable=False, index=True)
    pwd = Column(String(256), nullable=False)
    name = Column(String(64), default='')
    phone = Column(String(64), default='')
    email = Column(String(64), default='')
    address = Column(String(255), default='')
    is_vip = Column(Boolean, default=False)
    is_valid = Column(Boolean, default=True)

    def __repr__(self):
        return f'<User {self.id} {self.uname}>'
