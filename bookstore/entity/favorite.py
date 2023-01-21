from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer

from bookstore.application import db
from bookstore.util.result import model2dict


class Favorite(db.Model):  # type: ignore
    __tablename__ = 'favorite'
    uid = Column(Integer, ForeignKey("user.id"), primary_key=True)
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    add_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    book = db.relationship('Book', uselist=False)

    def to_dto(self):
        dto = {
            "book": model2dict(self.book),
        }
        return dto