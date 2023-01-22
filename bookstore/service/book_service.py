from typing import List

from sqlalchemy import and_, or_

from bookstore.application import db
from bookstore.entity import Book, Category


def get_book_by_id(bid: int) -> Book:
    return db.session.query(Book).get(bid)


def get_books_by_id(bids: List[int]) -> List[Book]:
    return db.session.query(Book).filter(Book.bid.in_(bids)).all()


def filter_books_by_category(cid: int):
    descendants = db.session.query(Category).get(cid).get_descendants()
    # return db.session.query(Book).filter(   )
    # 每个Book类对象有一个categories属性，存了它所有分类
    # 只要有一个分类的id在descendants中，那么就把它加入结果
    return db.session.query(Book)  # 这是一个暂时替代的


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
