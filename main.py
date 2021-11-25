from typing import List
from flask import Flask, request, render_template, url_for, abort, redirect
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, current_user
from flask_login.utils import login_user, logout_user
from flask_wtf import form
from werkzeug.security import check_password_hash, generate_password_hash
from form_handel import SignupForm
from db_handel import db, User, Task, Alert, TaskList
from datetime import datetime


# -------------------------------- GLOBALS -------------------------------------
home_page_list_name = ""

app = Flask(__name__)
app.config["SECRET_KEY"] = "RABIH's RASK"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/rask_users.db"

Bootstrap(app)
login_manager = LoginManager(app)
with app.app_context():
    db.init_app(app)
    # db.create_all()


@ login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)


@ app.route("/")
def home():
    return render_template("index.html")


@ app.route("/set-alert", methods=["POST"])
def set_alert():
    task_id = request.form["taskId"]

    task_has_alert = Alert.query.filter_by(task_id=task_id).first()
    alert_date_time = request.form["alertDateTime"]
    selected_task = Task.query.get(task_id)
    if not task_has_alert:
        if not alert_date_time == "":
            new_alert = Alert(
                user_email=current_user.email,
                task_id=task_id,
                message=selected_task.text,
                date_time=alert_date_time
            )
            selected_task.alert_date = alert_date_time.split("T")[0]
            selected_task.alert_time = alert_date_time.split("T")[1]
            db.session.add(new_alert)
    else:
        if alert_date_time == "":
            alert_to_remove = Alert.query.filter_by(task_id=task_id).first()
            db.session.delete(alert_to_remove)
            selected_task.alert_date = "none"
            selected_task.alert_time = "none"
        else:
            task_has_alert.date_time = alert_date_time
            selected_task.alert_date = alert_date_time.split("T")[0]
            selected_task.alert_time = alert_date_time.split("T")[1]

    db.session.commit()
    return ""


@ app.route("/add-new-task/<list_id>", methods=["POST"])
def add_task(list_id):
    try:
        task_text = request.form["userTask"]
        new_task = Task(
            creation_date=datetime.now(),
            text=task_text,
            list_id=list_id,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(new_task)
        db.session.commit()
    except KeyError:
        pass
    return redirect(url_for('task_lists', list_id=list_id))


@ app.route("/<list_id>/task-lists", methods=["GET", "POST"])
def task_lists(list_id):
    if not current_user.is_authenticated:
        global home_page_list_name
        home_page_list_name = request.form.get("listName")
        print(home_page_list_name)
        return redirect(url_for('signup', form=SignupForm()))
    task_id = request.form.get("task_id")
    due_date = request.form.get("name")
    if not due_date:
        due_date = "Add Due Date"
    if due_date and task_id:
        selected_task = Task.query.get(task_id)
        selected_task.due_date = due_date
        db.session.commit()
    task_to_delete_id = request.form.get("delete_task_id")
    if task_to_delete_id:
        task_to_delete = Task.query.get(task_to_delete_id)
        task_alert_to_remove = Alert.query.filter_by(
            task_id=task_to_delete_id).first()
        if task_alert_to_remove:
            db.session.delete(task_alert_to_remove)
        db.session.delete(task_to_delete)
        db.session.commit()
    if current_user.is_authenticated:
        list_name = TaskList.query.get(list_id).name
        user_lists = TaskList.query.filter_by(user_id=current_user.id).all()
        user_active_tasks = Task.query.filter_by(
            user_id=current_user.id, list_id=list_id, is_done=False)
        user_done_tasks = Task.query.filter_by(
            user_id=current_user.id, list_id=list_id, is_done=True)
    else:
        list_name = ""
        user_lists = []
    return render_template("task_lists.html", user_active_tasks=user_active_tasks, user_done_tasks=user_done_tasks, list_id=list_id,
                           new_list_name=list_name, user_lists=user_lists, active_done_margin=len(list(user_active_tasks)))


@ app.route("/ceck-task", methods=["POST"])
def check_task():
    task_id = request.form["taskId"]
    checked_task = Task.query.get(task_id)
    checked_task.is_done = True if checked_task.is_done == False else False
    db.session.commit()


@ app.route("/update-list-name", methods=["POST"])
def update_list_name():
    new_list_name = request.form["newName"]
    list_id = request.form["listId"]
    list = TaskList.query.get(list_id)
    list.name = new_list_name
    db.session.commit()


@ app.route("/<list_id>/del-list")
def delete_task_list(list_id):
    list_to_delete = TaskList.query.get(list_id)
    list_tasks = Task.query.filter_by(list_id=list_id).all()
    for task in list_tasks:
        alert = Alert.query.filter_by(task_id=task.id).first()
        if alert:
            db.session.delete(alert)
    for task in list_tasks:
        db.session.delete(task)
    db.session.delete(list_to_delete)
    db.session.commit()
    return redirect(url_for("manage_lists"))


@ app.route("/manage-lists")
def manage_lists():
    user_lists = TaskList.query.filter_by(user_id=current_user.id).all()
    return render_template("manage_lists.html", user_task_lists=user_lists)


@ app.route("/new-list", methods=["POST"])
def new_list():
    if request.method == "POST":
        list_name = request.form["listName"]
        new_list = TaskList(
            user_id=current_user.id if current_user.is_authenticated else None,
            name=list_name
        )
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for("task_lists", list_id=new_list.id))


@ app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(
            name=form.name.data,
            email=form.email.data.lower(),
            password=generate_password_hash(
                form.password.data, "pbkdf2:sha256", 8)
        )
        db.session.add(new_user)
        db.session.commit()
        new_users_list = TaskList(
            user_id=new_user.id,
            name="New List" if not home_page_list_name else home_page_list_name
        )
        db.session.add(new_users_list)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('task_lists', list_id=new_users_list.id))

    return render_template("sign_up.html", form=form)


@ app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_email = request.form["uEmail"].lower()
        user_password = request.form["uPassword"]
        user = User.query.filter_by(email=user_email).first()
        if user:
            if check_password_hash(user.password, user_password):
                login_user(user)
                return redirect(url_for("manage_lists"))

            return "<h1> password incorrect. </h1>"
        return "<h1> User not found. </h1>"

    return render_template("login.html")


@ app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
