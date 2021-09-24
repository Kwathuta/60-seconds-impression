from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    """
    User class to define user objects
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError("You cannot read the password attribute")

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f"User {self.username}"


class Impression(db.Model):
    __tablename__ = "impressions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    post = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    time = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(255), index=True, nullable=False)
    like = db.relationship("Like", backref="impression", lazy="dynamic")
    dislike = db.relationship("Dislike", backref="impression", lazy="dynamic")

    def save_impression(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"Impression {self.post}"
