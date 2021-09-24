from flask import render_template, redirect, url_for, abort, request
from . import main
from flask_login import login_required, current_user
from ..models import User, Impression, Comment, Like, Dislike
from .forms import UpdateProfile, ImpressionForm, CommentForm
from .. import db, photos


@main.route("/")
def index():
    impressions = Impression.query.all()
    interviews = Impression.query.filter_by(category="Interview").all()
    social = Impression.query.filter_by(category="Social").all()
    promotion = Impression.query.filter_by(category="Promotion").all()
    return render_template(
        "index.html",
        impressions=impressions,
        interviews=interviews,
        social=social,
        promotion=promotion,
    )


@main.route("/new_impression", methods=["GET", "POST"])
@login_required
def new_impression():
    form = ImpressionForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user
        new_impression_object = Impression(
            post=post,
            user_id=current_user._get_current_object().id,
            category=category,
            title=title,
        )
        new_impression_object.save_impression()
        return redirect(url_for("main.index"))

    return render_template("new_impression.html", form=form)


@main.route("/comments/<int:impression_id>", methods=["POST", "GET"])
@login_required
def comment(impression_id):
    form = CommentForm()
    impression = Impression.query.get(impression_id)
    all_comments = Comment.query.filter_by(impression_id=impression_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        impression_id = impression_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(
            comment=comment, user_id=user_id, impression_id=impression_id
        )
        new_comment.save_comment()
        return redirect(url_for(".comment", impression_id=impression_id))
    return render_template(
        "comment.html", form=form, impression=impression, all_comments=all_comments
    )


@main.route("/user/<name>")
def profile(name):
    user = User.query.filter_by(username=name).first()
    user_id = current_user._get_current_object().id
    posts = Impression.query.filter_by(user_id=user_id).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user, posts=posts)


@main.route("/user/<name>/updateprofile", methods=["POST", "GET"])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username=name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_user()
        return redirect(url_for(".profile", name=name))
    return render_template("profile/update.html", form=form)


@main.route("/user/<name>/update/avatar", methods=["POST"])
@login_required
def update_avatar(name):
    user = User.query.filter_by(username=name).first()
    if "photo" in request.files:
        filename = photos.save(request.files["photo"])
        path = f"photos/{filename}"
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for("main.profile", name=name))


@main.route("/like/<int:id>", methods=["POST", "GET"])
@login_required
def like(id):
    get_impressions = Like.get_likes(id)
    valid_string = f"{current_user.id}:{id}"
    for impression in get_impressions:
        to_str = f"{impression}"
        print(valid_string + " " + to_str)
        if valid_string == to_str:
            return redirect(url_for("main.index", id=id))
        else:
            continue
    new_like = Like(user=current_user, impression_id=id)
    new_like.save_like()
    return redirect(url_for("main.index", id=id))


@main.route("/dislike/<int:id>", methods=["POST", "GET"])
@login_required
def dislike(id):
    impression = Dislike.get_dislikes(id)
    valid_string = f"{current_user.id}:{id}"
    for i in impression:
        to_str = f"{i}"
        print(valid_string + " " + to_str)
        if valid_string == to_str:
            return redirect(url_for("main.index", id=id))
        else:
            continue
    new_dislike = Dislike(user=current_user, impression_id=id)
    new_dislike.save_dislike()
    return redirect(url_for("main.index", id=id))
