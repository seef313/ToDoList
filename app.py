"""
Key Features:

User sign up/sign in -x 
Create, edit, and delete to-dos
Set due-dates for to-dos
Ability to order to-dos
Marking to-dos as complete
"""
import models
from flask import Flask, redirect, url_for, render_template, request
from models import db, ToDO, User, LoginForm, RegisterForm, UpdateForm
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy import inspect


# Flask
app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00"
app.config["DEBUG"] = True

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt = Bcrypt(app)
# models.ToDO(db.Model)
db.create_all()

# login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Login page to manage users
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("index"))
            else:
                flash("wrong Password")
    return render_template("login.html", form=form)


# Index page will hold all the tasks for task list
@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """
    To-Do app page
    """
    # tasks = models.ToDO(db.Model).query.all()
    tasks = models.ToDO(db.Model).query.filter_by(user_id=current_user.id)
    return render_template("index.html", tasks=tasks)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/task", methods=["POST"])
def add_task():
    item = request.form["item"]
    dueDate = request.form["dueDate"]
    user_id = current_user.id

    if not item:
        return "Error"
    if current_user.is_authenticated:
        user_id = current_user.id
    new_task = ToDO(item, dueDate, user_id)
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:task_id>", methods=["POST", "GET"])
@login_required
def update_task(task_id):
    task = ToDO.query.filter_by(id=task_id).first()
    print(task)

    form = UpdateForm()
    if form.taskString.data != None:
        task.item = form.taskString.data
        db.session.commit()

    return render_template("update.html", task=task, id=task_id, form=form)


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = ToDO.query.get(task_id)
    if not task:
        return redirect("/")

    db.session.delete(task)
    db.session.commit()
    return redirect("/")


@app.route("/done/<int:task_id>")
def resolve_task(task_id):
    task = ToDO.query.get(task_id)

    if not task:
        return redirect("/")
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect("/")


@app.cli.command("initdb")
def reset_db():
    print("resetting db")
    from models import db, ToDO, User

    db.drop_all()
    # from models import db, ToDO, User
    import models

    db.create_all()
    db.session.add(User(username="bob123", password=bytes("password", encoding="utf8")))
    db.session.add(
        User(username="BigBob1", password=bytes("passWARD", encoding="utf8"))
    )
    db.session.add(
        User(username="LittleBob1", password=bytes("mustard1", encoding="utf8"))
    )

    db.session.commit()
    # import models


if __name__ == "__main__":
    app.run(port=3000)
