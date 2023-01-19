from typing import List

from sqlalchemy import and_, or_

from bookstore.application import db
from bookstore.entity.book import Book


def search_and(tit: str, auth: str, pub: str, abs: str) -> List[Book]:
    book_get = db.session.query(Book).filter(
        and_(
            Book.name.like('%' + tit + '%'),
            Book.author.like('%' + auth + '%'),
            Book.publisher.like('%' + pub + '%'),
            Book.desc.like('%' + abs + '%'),
        )
    ).all()
    return book_get


def search_or(kw: str) -> List[Book]:
    book_get = db.session.query(Book).filter(
        or_(
            Book.name.like('%' + kw + '%'),
            Book.author.like('%' + kw + '%'),
            Book.publisher.like('%' + kw + '%'),
            Book.desc.like('%' + kw + '%'),
        )
    ).all()
    return book_get
