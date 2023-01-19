import random

import pandas as pd
from sqlalchemy import Column, Integer, Numeric, String, Text

from bookstore.application import db


class Book(db.Model):  # type: ignore
    __tablename__ = 'book'
    __table_args__ = {"extend_existing": True}

    bid = Column(Integer, primary_key=True, nullable=False)
    cover = Column(String(255))
    name = Column(String(255))
    author = Column(String(255))
    publisher = Column(String(255))
    publishDate = Column(String(32))
    desc = Column(Text)
    price = Column(Numeric(10, 2, asdecimal=False))
    originalPrice = Column(Numeric(10, 2, asdecimal=False))

    @staticmethod
    def init():
        data = pd.read_csv("book.csv").drop(columns="price")
        db.session.add_all([
            Book(
                **item.to_dict(),
                price=random.randint(100, 500) / 10,
                originalPrice=random.randint(300, 800) / 10,
                publishDate=f"{random.randint(2010, 2020)}年{(random.randint(1,12))}月"
            ) for _, item in data.iterrows()
        ])
        db.session.commit()

    def to_dto(self):
        return self
