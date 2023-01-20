from flask import request

from bookstore.application import app, db
from bookstore.entity.book import Book
from bookstore.entity.comment import Comment
from bookstore.service.book_service import search_and, search_or
from bookstore.util.paging import paging
from bookstore.util.result import Result


@app.route('/api/book/comments/c<bid>', methods=['GET'])
def get_comments(bid: str):
    bid_ = int(bid)
    comments = db.session.query(Comment).filter(Comment.bid == bid_).all()
    return Result.success("", comments)


@app.route('/api/book/comments/post', methods=['POST'])
def post_comment():
    bid = request.json.get("bid")
    star = request.json.get("star")
    content = request.json.get("content")
    '''
    TODO
    在comment表中插入一条评论
    
    '''

    return Result.success("成功发布评论")