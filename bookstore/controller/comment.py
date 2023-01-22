from flask import request

from bookstore.application import app, db
from bookstore.entity import Comment
from bookstore.util.result import Result


@app.route('/api/book/comments/c<bid>', methods=['GET'])
def get_comments(bid: str):
    bid_ = int(bid)
    comments = db.session.query(Comment).filter(Comment.bid == bid_).all()
    return Result.success("", comments)


@app.route('/api/book/comments/post', methods=['POST'])
def post_comment():
    bid = request.json.get("bid")  # type:ignore
    star = request.json.get("star")  # type:ignore
    content = request.json.get("content")  # type:ignore
    '''
    TODO
    在comment表中插入一条评论
    
    '''

    return Result.success("成功发布评论")