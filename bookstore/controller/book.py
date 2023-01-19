from flask import request

from bookstore.application import app
from bookstore.entity.book import Book
from bookstore.service.book_service import search_and, search_or
from bookstore.util.result import Result


@app.route('/api/book/list', methods=['GET'])
def search_books():
    app.logger.info(request.args)
    args = request.args
    keyword = args.get('keyword')

    if keyword:
        result = search_or(keyword)
    else:
        result = search_and(
            tit=args.get("title", ""),
            auth=args.get("author", ""),
            pub=args.get("publisher", ""),
            abs=args.get("desc", "")
        )

    result = map(Book.to_dto, result)

    return Result.success("", result)
