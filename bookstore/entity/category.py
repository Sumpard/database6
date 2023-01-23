from typing import List
from sqlalchemy import Column, ForeignKey, Integer, String

from bookstore.application import db

CategoryBook = db.Table(
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
    book = db.relationship('Book', backref='categories', secondary=CategoryBook)

    def to_dto(self):
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
            "children_id": [c.id for c in self.children],
        }

    def expand_dto(self):
        return {
            "id": self.id,
            "name": self.name,
            "children": list(map(Category.expand_dto, self.children)),
        }

    def get_descendants(self) -> List[int]:
        return sum((c.get_descendants() for c in self.children), []) + [self.id]

    def get_books_of_category(self):
        return list(self.book) + sum((c.get_books_of_category() for c in self.children), [])
