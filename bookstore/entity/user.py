from bookstore.application import db


class User(db.Model):  # type: ignore
    __tablename__ = 'user'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    uname = db.Column(db.String(64), nullable=False)
    pwd = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(64), default='')
    phone = db.Column(db.String(64), default='')
    email = db.Column(db.String(64), default='')
    address = db.Column(db.String(255), default='')
    is_vip = db.Column(db.Boolean, default=False)
    is_valid = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.id} {self.uname}>'
