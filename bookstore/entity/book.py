from numpy import average
from sqlalchemy import Column, Date, Integer, Numeric, String, Text

from bookstore.application import db
from bookstore.entity.comment import Comment
from bookstore.util.result import model2dict


class Book(db.Model):  # type: ignore
    __tablename__ = 'book'
    __table_args__ = {"extend_existing": True}

    bid = Column(Integer, primary_key=True, nullable=False)
    cover = Column(String(255))
    name = Column(String(255))
    author = Column(String(255))
    publisher = Column(String(255))
    publishDate = Column(Date)
    desc = Column(Text)
    price = Column(Numeric(10, 2, asdecimal=False))
    originalPrice = Column(Numeric(10, 2, asdecimal=False))

    def to_dto(self):
        comments = db.session.query(Comment).filter(Comment.bid == self.bid).all()
        return {
            **model2dict(self),
            "rating": average([c.rating for c in comments]),
            "numComments": len(comments),
        }
