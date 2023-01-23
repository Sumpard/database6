from flask import request
from flask_login import current_user, login_required

from bookstore.application import app, db
from bookstore.entity.comment import Comment
from bookstore.util.result import Result, model2dict


@app.route('/api/book/comments/c<bid>', methods=['GET'])
def get_comments(bid: str):
    bid_ = int(bid)
    comments = db.session.query(Comment).filter(Comment.bid == bid_).all()
    return Result.success("", comments)


@app.route('/api/book/comments/post', methods=['POST'])
@login_required
def post_comment():
    data = request.json or {}

    comment = Comment(
        uid=current_user.id,  # type:ignore
        uname=current_user.uname,  # type:ignore
        bid=data["bid"],
        rating=data["star"],
        content=data["content"],
    )

    db.session.add(comment)
    db.session.commit()  # 不知道为啥，这句执行完后无法从result上获取__dict__内容了

    app.logger.info(comment.id)  # 貌似写了这句就能正常获取__dict__了

    return Result.success("成功发布评论", comment)