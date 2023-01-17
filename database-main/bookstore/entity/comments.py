from application import db
from entity.user import User
import random


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    uid = db.Column(db.String(64), nullable=False)
    bid = db.Column(db.String(64), nullable=False)
    rating = db.Column(db.Integer, default=5)
    comment = db.Column(db.String(255))
    #items= db.relationship()

    def __repr__(self):
        return f'<Comments {self.id}>'

    def generate_data(t):
        id = t+1
        uid = random.randint(1, 100)
        """ user_exists = True
            while (user_exists):
                uid = random.randint(1, 100)
                user_exists = db.session.query(
                    User).filter(User.id == uid).first() """
        bid = random.randint(1, 100)
        rating = random.randint(3, 5)
        commentslist = ["好评，孩子很喜欢！！",
                        "特殊时期，虽然等了很久，但终于还是在未开学前收到书本，是正品，太赞了",
                        "好书值得推荐，学习有一段时间了，非常棒的一本书，两全其美，点赞",
                        "很厚实的两本书，质量不错，每首诗都配有插图，值得购买",
                        "纸质较好，印刷质量也不错，价格也公道，物流很快给个好评！物品整体是不错的。",
                        "预售的，所以等了好久，不过也值了，还送了赠品，纸张好，内容清晰",
                        "不错!是正版噢，质量自然不用说!店家很贴心还送了口罩和小本子!满意，下次有需要还会来",
                        "物流给力！包装完好！收到孩子就开心的拆开了，书印刷很好，正版无疑！一起买了四本，给孩子在假期补充点精神食粮！活动很合适！值得购买！"]
        comment = random.choices(commentslist)
        info_list = [id, uid, bid, rating, comment]
        return info_list

    def add_data(t):
        for i in range(t):
            info = Comments.generate_data(i)
            commnet=Comments(id=info[0], uid=info[1], bid=info[2],rating=info[3],
                comment=info[4])
            db.session.add(commnet)
            db.session.commit()