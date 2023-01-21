from typing import List

from bookstore.application import db
from bookstore.entity.shopping_cart import ShoppingCart


def remove_cart_books_by_bid(uid: int, bids: List[int]):
    records = db.session.query(ShoppingCart).filter_by(uid=uid).filter(ShoppingCart.bid.in_(bids)).all()
    for r in records:
        db.session.delete(r)
    db.session.commit()
