from . import db, login_manager
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
    impressions = db.relationship("Impression", backref="user", lazy="dynamic")
    comment = db.relationship("Comment", backref="user", lazy="dynamic")
    like = db.relationship("Like", backref="user", lazy="dynamic")
    dislike = db.relationship("Dislike", backref="user", lazy="dynamic")

    @property
    def password(self):
        raise AttributeError("You cannot read the password attribute")

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

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


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    imression_id = db.Column(db.Integer, db.ForeignKey("impressions.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, impression_id):
        comments = Comment.query.filter_by(impression_id=impression_id).all()
        return comments

    def __repr__(self):
        return f"comment:{self.comment}"


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    impression_id = db.Column(db.Integer, db.ForeignKey("impressions.id"))

    def save_like(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_likes(cls, like_id):
        like = Like.query.filter_by(impression_id=like_id).all()
        return like

    def __repr__(self):
        return f"{self.user_id}:{self.impression_id}"


class Dislike(db.Model):
    __tablename__ = "dislikes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    impression_id = db.Column(db.Integer, db.ForeignKey("impressions.id"))

    def save_dislike(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_dislikes(cls, dislike_id):
        dislike = Dislike.query.filter_by(impression_id=dislike_id).all()
        return dislike

    def __repr__(self):
        return f"{self.user_id}:{self.impression_id}"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
