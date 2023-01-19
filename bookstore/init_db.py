import random
import numpy as np

import pandas as pd

from bookstore.application import app, db
from bookstore.entity.book import Book
from bookstore.entity.comment import Comment
from bookstore.entity.user import User

N_USERS = 100
N_BOOKS = 0

users = []


def init_users():
    from faker import Faker
    fake = Faker(["zh_CN"])
    Faker.seed(1919810)
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
    db.session.add_all(users)
    db.session.commit()


def init_books():
    data = pd.read_csv("book.csv").drop(columns="price")
    global N_BOOKS
    N_BOOKS = data.shape[0]
    db.session.add_all(
        Book(
            **item.to_dict(),
            price=random.randint(100, 500) / 10,
            originalPrice=random.randint(300, 800) / 10,
            publishDate=f"{random.randint(2010, 2020)}年{(random.randint(1,12))}月"
        ) for _, item in data.iterrows()
    )
    db.session.commit()


def init_comments():
    comments_list = [
        "好评，孩子很喜欢！！", "特殊时期，虽然等了很久，但终于还是在未开学前收到书本，是正品，太赞了", "好书值得推荐，学习有一段时间了，非常棒的一本书，两全其美，点赞",
        "很厚实的两本书，质量不错，每首诗都配有插图，值得购买", "纸质较好，印刷质量也不错，价格也公道，物流很快给个好评！物品整体是不错的。", "预售的，所以等了好久，不过也值了，还送了赠品，纸张好，内容清晰",
        "不错!是正版噢，质量自然不用说!店家很贴心还送了口罩和小本子!满意，下次有需要还会来",
        "物流给力！包装完好！收到孩子就开心的拆开了，书印刷很好，正版无疑！一起买了四本，给孩子在假期补充点精神食粮！活动很合适！值得购买！"
    ]
    db.session.add_all(
        Comment(
            uid=users[i].id,  # type: ignore
            uname=users[i].uname,  # type: ignore
            bid=random.randint(1, N_BOOKS),
            rating=random.randint(1, 5),
            content=random.choice(comments_list),
        ) for i in np.random.randint(0, N_USERS, 1000)
    )
    db.session.commit()


def init_all():
    db.drop_all()
    db.create_all()
    init_users()
    init_books()
    init_comments()