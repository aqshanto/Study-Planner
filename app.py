import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

from models import User, db

# Read the .env file so os.getenv can see SECRET_KEY.
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///planner.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect the database object from models.py to this app.
db.init_app(app)

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


@app.route("/dashboard")
@login_required
def dashboard():
    # Placeholder for now - task features come later.
    return render_template("dashboard.html")


if __name__ == "__main__":
    # Create planner.db and its tables the first time the app starts.
    with app.app_context():
        db.create_all()
    app.run(debug=True)
