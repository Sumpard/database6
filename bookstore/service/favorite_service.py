from typing import List

from bookstore.application import db
from bookstore.entity import Favorite
from bookstore.service.book_service import get_book_by_id


def add_book_to_favorites(uid: int, bid: int, delay_commit: bool = False):
    ac = db.session.query(Favorite).get({"uid": uid, "bid": bid})
    if ac:
        return None
    else:
        ac = Favorite(bid=bid, uid=uid, book=get_book_by_id(bid))
        db.session.add(ac)
    if not delay_commit:
        db.session.commit()
    return ac


def remove_favorites_by_bid(uid: int, bids: List[int]):
    records = db.session.query(Favorite).filter_by(uid=uid).filter(Favorite.bid.in_(bids)).all()
    for r in records:
        db.session.delete(r)
    db.session.commit()
