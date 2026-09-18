from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# One shared database object. app.py connects it to the app with db.init_app(app).
db = SQLAlchemy()


class User(UserMixin, db.Model):
    """A person who can log in. UserMixin gives Flask-Login the helpers it needs
    (is_authenticated, get_id, ...) so we don't have to write them."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # One user has many tasks. backref="user" lets us write task.user later.
    tasks = db.relationship("Task", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"


class Task(db.Model):
    """A study task. Not used yet - the task features come in a later step."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(80))
    deadline = db.Column(db.Date)
    priority = db.Column(db.String(10))  # "low" | "medium" | "high"
    status = db.Column(db.String(10), nullable=False, default="pending")

    # Each task belongs to exactly one user.
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Task {self.title}>"
