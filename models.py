from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """ Table for users """

    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def get_id(self):
        return (self.id)


class Reservations(db.Model):
    """save requested json file for each quiz"""

    __tablename__ = "reservations"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String())
    date = db.Column(db.String())
    guest_num = db.Column(db.String())
    customer_name = db.Column(db.String())


    def get_id(self):
        return (self.id)

class Foods(db.Model):
    """save requested json file for each quiz"""

    __tablename__ = "foods"
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String())
    food_cal = db.Column(db.String())
    food_ing = db.Column(db.String())
    pic_src = db.Column(db.String())


    def get_id(self):
        return (self.id)


class Reviews(db.Model):
    """save requested json file for each quiz"""

    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    date = db.Column(db.String())
    reviews = db.Column(db.String())


    def get_id(self):
        return (self.id)
