from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from bookstore.application import db
from bookstore.util.result import model2dict


class Order(db.Model):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey('user.id'))
    create_time = Column(DateTime)
    address = Column(String(255), default='')
    state = Column(Integer, default=0)
    price = Column(Numeric(10, 2))
    items = db.relationship('OrderBook', cascade="all,delete")

    def to_dto(self):
        print(self.items)
        dto: dict = model2dict(self, is_simple=True)
        dto["items"] = list(map(OrderBook.to_dto, self.items))
        return dto


class OrderBook(db.Model):
    __tablename__ = 'order_book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    oid = Column(Integer, ForeignKey('order.id'))
    bid = Column(Integer, ForeignKey('book.bid'))
    price = Column(Numeric(10, 2))
    book = db.relationship('Book', backref='orders')

    def to_dto(self):
        dto = model2dict(self)
        dto["book"] = model2dict(self.book)
        return dto