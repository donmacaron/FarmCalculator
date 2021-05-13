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
        return f"User('{self.username}'"


# class Group(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     group_number = db.Column(db.String(20), unique=True, nullable=False)
#     file = db.Column(db.String(20), unique=True, nullable=False)

#     def __repr__(self):
#         return f"Group('{self.group_number}'"
