from typing import List

from bookstore.application import db
from bookstore.entity import ShoppingCart
from bookstore.service.book_service import get_book_by_id


def add_book_to_cart(uid: int, bid: int, count: int = 1, allow_stack: bool = True, delay_commit: bool = False):
    ac = db.session.query(ShoppingCart).get({"uid": uid, "bid": bid})
    if ac:
        if not allow_stack:
            return None
        ac.count += count
    else:
        ac = ShoppingCart(bid=bid, uid=uid, count=count, book=get_book_by_id(bid))
        db.session.add(ac)
    if not delay_commit:
        db.session.commit()
    return ac


def remove_cart_books_by_bid(uid: int, bids: List[int]):
    records = db.session.query(ShoppingCart).filter_by(uid=uid).filter(ShoppingCart.bid.in_(bids)).all()
    for r in records:
        db.session.delete(r)
    db.session.commit()
