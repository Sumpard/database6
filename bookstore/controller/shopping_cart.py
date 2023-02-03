from flask import request
from flask_login import current_user, login_required

from bookstore.application import app, db
from bookstore.entity.shopping_cart import ShoppingCart
from bookstore.service.book_service import get_book_by_id
from bookstore.service.favorite_service import add_book_to_favorites
from bookstore.service.shopping_cart_service import add_book_to_cart, get_cart_book_by_bid, remove_cart_books_by_bid
from bookstore.util.result import Result


@app.route('/api/shopping_cart', methods=['GET'])
@login_required
def get_cart():
    uid = current_user.id  # type: ignore
    shoppingCart = db.session.query(ShoppingCart).filter_by(uid=uid).order_by(ShoppingCart.bid).all()
    return Result.success("", list(map(ShoppingCart.to_dto, shoppingCart)))


@app.route('/api/shopping_cart/add', methods=['POST'])
@login_required
def add_to_cart():
    uid = current_user.id  # type: ignore
    bid = request.json["bid"]  # type: ignore
    count = request.json["count"]  # type: ignore

    book = get_book_by_id(bid)
    if book.quantity < count:
        return Result.fail(f"库存不足！库存只有{book.quantity}本，但是您想要{count}本")

    ac = add_book_to_cart(uid, bid, count)
    if not ac:
        return Result.fail("加入购物车失败")

    return Result.success(f"成功加入购物车（当前数量：{ac.count}）")


@app.route('/api/shopping_cart/remove', methods=['POST'])
@login_required
def remove_from_cart():
    uid = current_user.id  # type: ignore
    bids = request.json["bids"]  # type: ignore
    remove_cart_books_by_bid(uid, bids)
    return Result.success("成功删除购物车物品")


@app.route('/api/shopping_cart/move', methods=['POST'])
@login_required
def move_items_to_favorites():
    uid = current_user.id  # type: ignore
    bids = request.json["bids"]  # type: ignore

    for b in bids:
        add_book_to_favorites(uid, b, delay_commit=True)
    db.session.commit()

    remove_cart_books_by_bid(uid, bids)

    return Result.success("成功将物品移入收藏夹")


@app.route('/api/shopping_cart/update', methods=['POST'])
@login_required
def update_item_count():
    uid = current_user.id  # type: ignore
    bid = request.json["bid"]  # type: ignore
    count = request.json["count"]  # type: ignore

    book = get_book_by_id(bid)
    if book.quantity < count:
        return Result.fail("库存不足！")

    item = get_cart_book_by_bid(uid, bid)
    item.count = count

    db.session.commit()

    return Result.success("")
