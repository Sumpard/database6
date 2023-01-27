from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from bookstore.application import db


class Comment(db.Model):  # type: ignore
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    uid = Column(Integer, ForeignKey("user.id"))
    uname = Column(String(64), ForeignKey("user.uname"))
    bid = Column(Integer, ForeignKey("book.bid"))
    rating = Column(Integer, default=5)  # 评分
    post_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 发布日期
    content = Column(Text, default="")  # 内容
    likes = Column(Integer, default=0)  # 点赞数
