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

    if db.session.query(Order).filter_by(uid=uid, state=0).first():
        return Result.fail("存在订单未结算，请先结算再下单！")

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

    # 更新数量
    for i in items:
        i.book.quantity -= i.count

    db.session.commit()

    return Result.success("成功创建订单")


@app.route('/api/order', methods=['GET'])
@login_required
def get_order():
    uid = current_user.id  # type: ignore

    # 目前只考虑获取第一单
    order = db.session.query(Order).filter_by(uid=uid, state=0).first()
    if order:
        return Result.success("", order.to_dto())

    return Result.success("", order)


@app.route('/api/order/submit', methods=['POST'])
@login_required
def submit_order():
    uid = current_user.id  # type: ignore

    order = db.session.query(Order).filter_by(uid=uid, state=0).first()
    order.state = 1
    db.session.commit()

    return Result.success("成功提交订单！")
