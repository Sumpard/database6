from sqlalchemy import Column, ForeignKey, Integer, String, Text

from bookstore.application import db


class Comment(db.Model):  # type: ignore
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    uid = Column(Integer, ForeignKey("user.id"))
    uname = Column(String(64), ForeignKey("user.uname"))
    bid = Column(Integer, ForeignKey("book.bid"))
    rating = Column(Integer, default=5)
    content = Column(Text, default="")

    def __repr__(self):
        return f'<Comment {self.id}>'
