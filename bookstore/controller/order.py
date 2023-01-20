from flask import request

from bookstore.application import app, db
from bookstore.entity.book import Book
from bookstore.entity.comment import Comment
from bookstore.service.book_service import search_and, search_or
from bookstore.util.paging import paging
from bookstore.util.result import Result


@app.route('/api/cart/<cid>', methods=['GET'])
def get_cart():

    return Result.success()
