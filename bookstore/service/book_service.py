from typing import List

from sqlalchemy import and_, or_

from bookstore.application import db
from bookstore.entity import Book, Category, CategoryBook


def get_book_by_id(bid: int) -> Book:
    return db.session.query(Book).get(bid)


def get_books_by_id(bids: List[int]) -> List[Book]:
    return db.session.query(Book).filter(Book.bid.in_(bids)).all()


def filter_books_by_category(cid: int):
    descendants = db.session.query(Category).get(cid).get_descendants()
    bids = db.session.query(CategoryBook.c["book_id"]).filter(CategoryBook.c["category_id"].in_(descendants))
    return db.session.query(Book).filter(Book.bid.in_(bids))


def filter_books_explicit(q, tit: str, auth: str, pub: str, abs: str) -> List[Book]:
    return q.filter(
        and_(
            Book.name.like('%' + tit + '%'),
            Book.author.like('%' + auth + '%'),
            Book.publisher.like('%' + pub + '%'),
            Book.desc.like('%' + abs + '%'),
        )
    )


def filter_books_fuzzy(q, kw: str) -> List[Book]:
    return q.filter(
        or_(
            Book.name.like('%' + kw + '%'),
            Book.author.like('%' + kw + '%'),
            Book.publisher.like('%' + kw + '%'),
        )
    )
