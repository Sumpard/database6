from sqlalchemy import and_
from sqlalchemy import or_
from application import app,db
from entity.book import Book

def Search_union(tit,auth,pub,abs):
    book_get = db.session.query(Book).filter(and_(Book.title.like('%'+tit+'%'),Book.author.like('%'+auth+'%')),
                                    Book.publisher.like('%'+pub+'%'),Book.abstract.like('%'+abs+'%')).all()
    print(book_get)
    #db.session.query(Book).filter(Book.bid==book_get[0])
    #print(111111111)
    return book_get


def Search_or(tit,auth,pub,abs):
    book_get = db.session.query(Book).filter(or_(Book.title.like('%'+tit+'%'),Book.author.like('%'+auth+'%'),
                                    Book.publisher.like('%'+pub+'%'),Book.abstract.like('%'+abs+'%'))).all()
    #db.session.excute()
    print(book_get)
    #print(2222222222)
    return book_get
