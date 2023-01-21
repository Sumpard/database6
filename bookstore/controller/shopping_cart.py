from flask import request
from flask_login import current_user, login_required

from bookstore.application import app, db
from bookstore.entity.shopping_cart import ShoppingCart
from bookstore.service.book_service import get_book_by_id
from bookstore.service.shopping_cart_service import remove_cart_books_by_bid
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
    ac = db.session.query(ShoppingCart).get({"uid": uid, "bid": bid})
    if ac:  # 若存在，则加count
        ac.count += count
    else:
        ac = ShoppingCart(bid=bid, uid=uid, count=count, book=get_book_by_id(bid))
        db.session.add(ac)
    db.session.commit()
    app.logger.info(type(ac.book.price))
    return Result.success(f"成功加入购物车（当前数量：{ac.count}）")


@app.route('/api/shopping_cart/remove', methods=['POST'])
@login_required
def remove_from_cart():
    uid = current_user.id  # type: ignore
    bids = request.json["bids"]  # type: ignore
    remove_cart_books_by_bid(uid, bids)
    return Result.success("成功删除购物车物品")
