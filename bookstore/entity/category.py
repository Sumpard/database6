from sqlalchemy import Column, ForeignKey, Integer, String

from bookstore.application import db

_middle = db.Table(
    "category_book",
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True),
    Column('book_id', Integer, ForeignKey('book.bid'), primary_key=True),
)


class Category(db.Model):  # type: ignore
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))
    parent_id = Column(Integer, ForeignKey('category.id'))
    parent = db.relationship('Category', backref='children', remote_side=[id])
    book = db.relationship('Book', backref='categories', secondary=_middle)
