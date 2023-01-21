from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from bookstore.application import db
from bookstore.util.result import model2dict


class ShoppingCart(db.Model):  # type: ignore
    __tablename__ = 'shopping_cart'
    uid = Column(Integer, ForeignKey("user.id"), primary_key=True)
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    count = Column(Integer, default=1)
    add_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    book = db.relationship('Book', uselist=False)

    def to_dto(self):
        dto = {
            "count": self.count,
            "book": model2dict(self.book),
        }
        return dto