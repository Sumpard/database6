from flask import request
from flask_login import current_user, login_required

from bookstore.application import app, db
from bookstore.entity.order import Order, OrderBook
from bookstore.entity.shopping_cart import ShoppingCart
from bookstore.service.shopping_cart_service import remove_cart_books_by_bid
from bookstore.util.result import Result


@app.route('/api/order/create', methods=['POST'])
@login_required
def create_order():
    uid = current_user.id  # type: ignore
    address = current_user.address  # type: ignore

    bids = request.json["bids"]  # type: ignore
    items = db.session.query(ShoppingCart).filter_by(uid=uid).filter(ShoppingCart.bid.in_(bids)).all()

    order = Order(
        uid=uid,
        address=address,
        payment=sum(i.book.price * i.count for i in items),
        items=[OrderBook(bid=i.book.bid, price=i.book.price, count=i.count, book=i.book) for i in items],
    )
    db.session.add(order)

    # 从购物车删除
    remove_cart_books_by_bid(uid, bids)

    db.session.commit()

    return Result.success("成功创建订单")
