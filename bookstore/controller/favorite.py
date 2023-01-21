from flask import request
from flask_login import current_user, login_required

from bookstore.application import app, db
from bookstore.entity import Favorite
from bookstore.service.book_service import get_book_by_id
from bookstore.service.favorite_service import add_book_to_favorites, remove_favorites_by_bid
from bookstore.service.shopping_cart_service import add_book_to_cart
from bookstore.util.result import Result


@app.route('/api/favorite', methods=['GET'])
@login_required
def get_favorites():
    uid = current_user.id  # type: ignore
    favorites = db.session.query(Favorite).filter_by(uid=uid).order_by(Favorite.bid).all()
    return Result.success("", list(map(Favorite.to_dto, favorites)))


@app.route('/api/favorite/add', methods=['POST'])
@login_required
def add_to_favorites():
    uid = current_user.id  # type: ignore
    bid = request.json["bid"]  # type: ignore

    if not add_book_to_favorites(uid, bid):
        return Result.fail("已收藏，不能重复加入！")

    return Result.success(f"成功加入收藏夹")


@app.route('/api/favorite/remove', methods=['POST'])
@login_required
def remove_from_favorites():
    uid = current_user.id  # type: ignore
    bids = request.json["bids"]  # type: ignore
    remove_favorites_by_bid(uid, bids)
    return Result.success("成功从收藏夹删除物品")


@app.route('/api/favorite/move', methods=['POST'])
@login_required
def move_favorites_to_cart():
    uid = current_user.id  # type: ignore
    bids = request.json["bids"]  # type: ignore

    for b in bids:
        add_book_to_cart(uid, b, allow_stack=False, delay_commit=True)
    db.session.commit()

    remove_favorites_by_bid(uid, bids)

    return Result.success("成功将物品移入购物车")
