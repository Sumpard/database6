import json
from sqlalchemy import Column, Date, Integer, Numeric, String, Text

from bookstore.application import db
from bookstore.entity.comment import Comment
from bookstore.util.result import model2dict


class Book(db.Model):  # type: ignore
    __tablename__ = 'book'
    __table_args__ = {"extend_existing": True}

    bid = Column(Integer, primary_key=True, autoincrement=True)
    cover = Column(String(255))  # 封面图片url
    name = Column(String(255))  # 书名/商品名
    author = Column(String(255))  # 作者
    publisher = Column(String(255))  # 出版社
    publishDate = Column(Date)  # 出版日期
    desc = Column(Text)  # 描述
    price = Column(Numeric(10, 2, asdecimal=False))  # 价格
    originalPrice = Column(Numeric(10, 2, asdecimal=False))  # 原价
    keys = Column(String(256))  # 关键词，如开本、页数

    def to_dto(self):
        comments = db.session.query(Comment).filter(Comment.bid == self.bid).all()
        numComments = len(comments)
        rating = sum(c.rating for c in comments) / numComments if numComments > 0 else None
        dto = {
            **model2dict(self),
            "rating": rating,
            "numComments": numComments,
        }
        keys = json.loads(self.keys)  # type: ignore
        dto["keys"] = dict(k.split("：") for k in keys)
        return dto
