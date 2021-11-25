from flask_sqlalchemy import SQLAlchemy
from flask_login.mixins import UserMixin


db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(500), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey("task_lists.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    creation_date = db.Column(db.String(500), nullable=False)
    text = db.Column(db.String(2000), nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.String(500), default="Add Due Date")
    alert_date = db.Column(db.String(500), default="none")
    alert_time = db.Column(db.String(100), default="none")


class TaskList(db.Model):
    __tablename__ = "task_lists"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String(500))


class Alert(db.Model):
    __tablename__ = "alerts"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))
    date_time = db.Column(db.String(500), nullable=False)
    user_email = db.Column(db.String(500), nullable=False)
    message = db.Column(db.String(2000), nullable=False)
