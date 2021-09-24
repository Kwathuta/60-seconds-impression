from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class UpdateProfile(FlaskForm):
    bio = TextAreaField(
        "Let people know a little bit more about you", validators=[DataRequired()]
    )
    submit = SubmitField("Save")


class ImpressionForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[
            ("Interview", "Interview"),
            ("Social", "Social"),
            ("Promotion", "Promotion"),
        ],
        validators=[DataRequired()],
    )
    post = TextAreaField("Your Impression", validators=[DataRequired()])
    submit = SubmitField("Impress")


class CommentForm(FlaskForm):
    comment = TextAreaField("Leave a comment", validators=[DataRequired()])
    submit = SubmitField("Comment")
