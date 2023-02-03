import json
import random
import sys
from collections import namedtuple
from datetime import datetime
from functools import reduce
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from bookstore.application import app, db
from bookstore.entity import *

N_USERS = 100

fake = Faker(["zh_CN"])
Faker.seed(1919810)

users = []
books = []


def initializer(f):
    def wrapped():
        db.session.add_all(f())
        db.session.commit()

    return wrapped


@initializer
def init_users():
    global users
    users = [
        User(
            id=i + 100,
            uname=fake.user_name(),
            pwd=fake.password(length=8, special_chars=False, digits=True, upper_case=True, lower_case=True),
            name=fake.name(),
            phone=fake.phone_number(),
            email=fake.email(),
            address=fake.address(),
            is_vip=random.choice((False, True)),
            is_valid=True,
        ) for i in range(N_USERS)
    ]
    return users


@initializer
def init_books():
    data = pd.read_csv("dangdang.csv")

    cates = data["cates"].tolist()
    root_cate = Category(name="图书")
    db.session.add(root_cate)

    CateTree = namedtuple("CateTree", ["value", "children"])

    cate_tree = CateTree(root_cate, {})

    for c0 in cates:
        for c1 in json.loads(c0):
            x = cate_tree
            for c2 in c1[1:]:
                if c2 not in x.children:
                    cc = Category(parent_id=x.value.id, name=c2, parent=x.value)
                    x.children[c2] = CateTree(cc, {})
                    db.session.add(cc)
                x = x.children[c2]

    db.session.commit()

    global books
    books = []
    for _, item in data.iterrows():
        c = json.loads(item["cates"])
        books.append(
            Book(
                name=item["书名"],
                cover=item["图片"],
                desc=item["desc"],
                author=item["作者"],
                publisher=item["出版社"],
                price=item["售价"][1 :],
                originalPrice=item["原价"][1 :],
                publishDate=datetime.strptime(item["出版日期"], "%Y-%m-%d"),
                quantity=random.randint(1, 100),
                keys=item["keys"],
                categories=[reduce(lambda x, y: x.children[y], c1[1 :], cate_tree).value for c1 in c],
            )
        )
    return books


@initializer
def init_comments():
    comments_list = [
        "好评，孩子很喜欢！！",
        "特殊时期，虽然等了很久，但终于还是在未开学前收到书本，是正品，太赞了",
        "好书值得推荐，学习有一段时间了，非常棒的一本书，两全其美，点赞",
        "很厚实的两本书，质量不错，每首诗都配有插图，值得购买",
        "纸质较好，印刷质量也不错，价格也公道，物流很快给个好评！物品整体是不错的。",
        "预售的，所以等了好久，不过也值了，还送了赠品，纸张好，内容清晰",
        "不错!是正版噢，质量自然不用说!店家很贴心还送了口罩和小本子!满意，下次有需要还会来",
        "物流给力！包装完好！收到孩子就开心的拆开了，书印刷很好，正版无疑！一起买了四本，给孩子在假期补充点精神食粮！活动很合适！值得购买！",
    ]
    return (
        Comment(
            uid=users[i].id,  # type: ignore
            uname=users[i].uname,  # type: ignore
            bid=random.randint(1, len(books)),
            rating=random.randint(3, 5),
            content=random.choice(comments_list),
            post_time=fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None),
            likes=random.randint(0, 100),
        ) for i in np.random.randint(0, N_USERS,
                                     len(books) * 5)
    )


def init_carts():
    ...


@initializer
def init_orders():
    orders = []
    for user in users:
        k = random.randint(1, 10)
        chosen_books = random.sample(books, k)
        ordered_books = [
            OrderBook(
                bid=book.bid,
                book=book,
                price=random.choice([book.price, book.originalPrice]),
                count=random.randint(1, 3),
            ) for book in chosen_books
        ]
        orders.append(
            Order(
                uid=user.id,
                create_time=fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None),
                address=fake.address(),
                payment=sum(b.price * b.count for b in ordered_books),
                items=ordered_books,
            )
        )
    return orders


def init_all():
    db.drop_all()
    db.create_all()
    init_users()
    init_books()
    init_comments()
    init_carts()
    init_orders()


if __name__ == '__main__':
    with app.app_context():
        init_all()
