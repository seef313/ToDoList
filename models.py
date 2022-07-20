import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, ValidationError

_timer = time.perf_counter()  # time.clock
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    # __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Binary(60), nullable=False)
    tasklistId = db.relationship("ToDO", backref="taskList", lazy=True)


class ToDO(db.Model):
    __tablename__ = "toDO"
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100))
    dueDate = db.Column(db.String(100))
    done = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, item, dueDate=None, user_id=""):
        self.item = item
        self.dueDate = dueDate
        self.done = False
        self.user_id = user_id

    def __repr__(self):
        # return '<Content %s Due Date: %s >' % self.item
        return f"ToDO('{self.item}''{self.dueDate}')"

    # pass


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Login")


# make update form
# update task and also change assignee?
class UpdateForm(FlaskForm):

    taskString = StringField(
        validators=[InputRequired()],
        render_kw={"placeholder": "Edit Task Here "},
    )

    # submit = SubmitField("Login")
