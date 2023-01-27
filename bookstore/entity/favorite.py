from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer

from bookstore.application import db
from bookstore.util.result import model2dict


class Favorite(db.Model):  # type: ignore
    __tablename__ = 'favorite'
    uid = Column(Integer, ForeignKey("user.id"), primary_key=True)
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    add_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 加入时间
    book = db.relationship('Book', uselist=False)  # 对应的书

    def to_dto(self):
        dto = {
            "book": model2dict(self.book),
        }
        return dto