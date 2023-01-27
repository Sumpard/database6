from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from bookstore.application import db
from bookstore.util.result import model2dict


class Order(db.Model):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, ForeignKey('user.id'))
    create_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 创建日期
    address = Column(String(255), default='')  # 配送地址
    state = Column(Integer, default=0)  # 状态，0表示未付款，1表示已付款
    payment = Column(Numeric(10, 2))  # 应付金额
    items = db.relationship('OrderBook', cascade="all,delete")

    def to_dto(self):
        print(self.items)
        dto: dict = model2dict(self, is_simple=True)
        dto["items"] = list(map(OrderBook.to_dto, self.items))
        return dto


class OrderBook(db.Model):
    __tablename__ = 'order_book'
    oid = Column(Integer, ForeignKey('order.id'), primary_key=True)
    bid = Column(Integer, ForeignKey('book.bid'), primary_key=True)
    price = Column(Numeric(10, 2))  # 购买单价
    count = Column(Integer)  # 数量
    book = db.relationship('Book', uselist=False)

    def to_dto(self):
        dto = model2dict(self)
        dto["book"] = model2dict(self.book)
        return dto