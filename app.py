import os
from datetime import date, datetime

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

from models import Task, User, db

# Read the .env file so os.getenv can see SECRET_KEY.
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY missing - create a .env file with SECRET_KEY=...")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///planner.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect the database object from models.py to this app.
db.init_app(app)

with app.app_context():
    db.create_all()

# Flask-Login keeps track of who is logged in.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # where to send visitors who must log in
login_manager.login_message = "Please log in first."


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login stores only the user id in the session cookie.
    On every request it calls this to turn that id back into a User object."""
    return db.session.get(User, int(user_id))


@app.route("/")
def home():
    # Logged in -> dashboard, otherwise -> login page.
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # All three fields are required.
        if not username or not email or not password:
            flash("Please fill in every field.", "danger")
            return render_template("signup.html")

        # Emails must be unique, so refuse one that is already taken.
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("That email is already registered. Try logging in.", "danger")
            return render_template("signup.html")

        # Never store the raw password - only its hash.
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()

        flash("Account created. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        # One message for both cases, so we don't reveal which emails exist.
        if user is None or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        login_user(user)  # this puts the user id into the session cookie
        flash(f"Welcome back, {user.username}!", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()  # clears the user id from the session
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# ---------------------------------------------------------------- task helpers


def get_owned_task(task_id):
    """Load one task, but only if it belongs to the logged-in user.
    Anything else is a 404 - we use 404 instead of 403 so we never hint that
    someone else's task with that id exists."""
    task = db.session.get(Task, task_id)
    if task is None or task.user_id != current_user.id:
        abort(404)
    return task


def read_task_form():
    """Pull the task fields out of a submitted form.
    Returns (values_dict, error_message). error_message is None when all is well."""
    title = request.form.get("title", "").strip()
    subject = request.form.get("subject", "").strip()
    deadline_text = request.form.get("deadline", "").strip()
    priority = request.form.get("priority", "medium")

    if not title:
        return None, "Title is required."

    if priority not in ("low", "medium", "high"):
        priority = "medium"

    # The date input sends "YYYY-MM-DD", or an empty string if left blank.
    deadline = None
    if deadline_text:
        try:
            deadline = datetime.strptime(deadline_text, "%Y-%m-%d").date()
        except ValueError:
            return None, "Please enter a valid deadline date."

    values = {
        "title": title,
        "subject": subject or None,
        "deadline": deadline,
        "priority": priority,
    }
    return values, None


# ----------------------------------------------------------------- task routes


@app.route("/dashboard")
@login_required
def dashboard():
    status = request.args.get("status")

    # Start from this user's tasks only - never the whole table.
    query = Task.query.filter_by(user_id=current_user.id)

    # Any other value (or none at all) means "show everything".
    if status in ("pending", "done"):
        query = query.filter_by(status=status)
    else:
        status = None

    # Soonest deadline first. The is_(None) key keeps undated tasks at the
    # bottom, because SQLite would otherwise sort empty deadlines to the top.
    tasks = query.order_by(Task.deadline.is_(None), Task.deadline.asc()).all()

    # today is used by the template to spot overdue tasks.
    return render_template(
        "dashboard.html", tasks=tasks, status=status, today=date.today()
    )


@app.route("/task/add", methods=["GET", "POST"])
@login_required
def task_add():
    if request.method == "POST":
        values, error = read_task_form()
        if error:
            flash(error, "danger")
            return render_template("task_form.html", task=None, heading="Add task")

        # The new task is tied to the logged-in user, not to anything the
        # browser sent us.
        task = Task(user_id=current_user.id, status="pending", **values)
        db.session.add(task)
        db.session.commit()

        flash("Task added.", "success")
        return redirect(url_for("dashboard"))

    return render_template("task_form.html", task=None, heading="Add task")


@app.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def task_edit(task_id):
    task = get_owned_task(task_id)  # 404s before we show or change anything

    if request.method == "POST":
        values, error = read_task_form()
        if error:
            flash(error, "danger")
            return render_template("task_form.html", task=task, heading="Edit task")

        # Copy the new values onto the task we already proved they own.
        task.title = values["title"]
        task.subject = values["subject"]
        task.deadline = values["deadline"]
        task.priority = values["priority"]
        db.session.commit()

        flash("Task updated.", "success")
        return redirect(url_for("dashboard"))

    # GET: the form is filled in from the task itself.
    return render_template("task_form.html", task=task, heading="Edit task")


@app.route("/task/<int:task_id>/delete", methods=["POST"])
@login_required
def task_delete(task_id):
    task = get_owned_task(task_id)
    db.session.delete(task)
    db.session.commit()

    flash("Task deleted.", "success")
    return redirect(url_for("dashboard", status=request.args.get("status")))


@app.route("/task/<int:task_id>/toggle", methods=["POST"])
@login_required
def task_toggle(task_id):
    task = get_owned_task(task_id)

    # Flip between the two states.
    task.status = "done" if task.status == "pending" else "pending"
    db.session.commit()

    return redirect(url_for("dashboard", status=request.args.get("status")))


if __name__ == "__main__":
    app.run(debug=True)