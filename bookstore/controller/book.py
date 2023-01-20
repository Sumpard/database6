from flask import request

from bookstore.application import app, db
from bookstore.entity.book import Book
from bookstore.entity.comment import Comment
from bookstore.service.book_service import search_and, search_or
from bookstore.util.paging import paging
from bookstore.util.result import Result


@app.route('/api/book/list', methods=['GET'])
def search_books():
    app.logger.info(request.args)
    args = request.args

    page = int(args.get('page', "1"))
    per_page = int(args.get('pageSize', "20"))

    keyword = args.get('keyword')

    if keyword:
        result = paging(search_or, page, per_page)(keyword)
    else:
        result = paging(search_and, page, per_page)(
            tit=args.get("name", ""),
            auth=args.get("author", ""),
            pub=args.get("publisher", ""),
            abs=args.get("desc", "")
        )

    result = {
        "items": list(map(Book.to_dto, result)),
        "page": result.page,  # 当前页
        "pages": result.pages,  # 页数
        "total": result.total,  # 总记录数
        "pageSize": result.per_page,  # 每页记录数
    }

    return Result.success("", result)


@app.route('/api/book/b<bid>', methods=['GET'])
def get_book_detail(bid: str):
    app.logger.info(type(bid))
    bid_ = int(bid)
    book = db.session.query(Book).filter(Book.bid == bid_).first()
    return Result.success("", book.to_dto())
