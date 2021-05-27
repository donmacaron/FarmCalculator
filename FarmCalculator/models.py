from datetime import datetime
from flask_login import UserMixin
from FarmCalculator import db
from FarmCalculator import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User '{self.username}'"


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    quarter = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"'{self.name}'"


class CurrentValues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rabbit_type = db.Column(db.String(20), unique=True, nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"'{self.rabbit_type}, {self.amount}'"


class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), unique=False, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    feed_type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)
    provider = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"'Тип: {self.type},\nПоставщик: {self.provider},\nТип Корма: {self.feed_type},\nСколько: {self.amount},\nКогда: {self.date}'"


# class Group(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     group_number = db.Column(db.String(20), unique=True, nullable=False)
#     file = db.Column(db.String(20), unique=True, nullable=False)

#     def __repr__(self):
#         return f"Group('{self.group_number}'"
