from flask import request
from flask_login import current_user

from bookstore.application import app, db
from bookstore.entity import Book
from bookstore.service.book_service import filter_books_by_category, filter_books_explicit, filter_books_fuzzy
from bookstore.service.favorite_service import is_in_favorites
from bookstore.util.paging import paging
from bookstore.util.result import Result


@app.route('/api/book/list', methods=['GET'])
def search_books():
    args = request.args

    page = int(args.get('page', "1"))
    per_page = int(args.get('pageSize', "20"))

    cate = int(args.get('category', '1'))
    keyword = args.get('keyword')

    q = filter_books_by_category(cate)

    if keyword:
        result = paging(filter_books_fuzzy, page, per_page)(q, keyword)
    else:
        result = paging(filter_books_explicit, page, per_page)(
            q,
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
    if current_user.is_authenticated:  # type: ignore
        uid = current_user.id  # type: ignore
        for i in result["items"]:
            i["favorite"] = is_in_favorites(uid, i["bid"])

    return Result.success("", result)


@app.route('/api/book/b<bid>', methods=['GET'])
def get_book_detail(bid: str):
    bid_ = int(bid)
    book = db.session.query(Book).filter(Book.bid == bid_).first()
    return Result.success("", book.to_dto())
