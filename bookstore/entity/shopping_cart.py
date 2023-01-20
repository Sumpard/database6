from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from bookstore.application import db


class ShoppingCart(db.Model):  # type: ignore
    __tablename__ = 'shopping_cart'
    uid = Column(Integer, ForeignKey("user.id"), primary_key=True)
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    add_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    book = db.relationship('Book', uselist=False)
