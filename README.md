# Study Planner

A small web app for keeping track of study tasks. You create an account, log in,
and manage your own list of tasks — each with a title, subject, deadline and
priority. Tasks can be marked done and switched back to pending, filtered by
status, and any task that is still pending after its deadline has passed is
highlighted in red so it is easy to spot.

Every user only ever sees their own tasks.

## Stack

- Python 3 (developed on 3.14)
- Flask
- Flask-SQLAlchemy (SQLite database, created automatically on first run)
- Flask-Login (sessions)
- Jinja2 templates
- Bootstrap 5, loaded from a CDN (nothing to install)
- python-dotenv for the secret key

## How to run it

```bash
# 1. Clone
git clone https://github.com/aqshanto/Study-Planner.git
cd Study-Planner

# 2. Create a virtual environment
python -m venv venv

#    Activate it — Windows:
venv\Scripts\activate
#    macOS / Linux:
source venv/bin/activate

# 3. Install the dependencies
pip install -r requirements.txt
```

**4. Create a `.env` file** in the project root with a secret key of your own:

```
SECRET_KEY=any-long-random-text-you-type-here
```

This file is deliberately not committed (it is listed in `.gitignore`), so every
clone needs its own. The app refuses to start without it and tells you so.

```bash
# 5. Run
python app.py
```

Then open <http://127.0.0.1:5000/>. You will be sent to the login page — use
**Sign up** to create an account first. The SQLite database is created at
`instance/planner.db` the first time the app starts; there is no migration step.

## Project layout

| Path | What it holds |
| --- | --- |
| `app.py` | Configuration, login setup, and all routes |
| `models.py` | The `User` and `Task` database tables |
| `templates/` | Jinja2 templates (`base.html` plus one per page) |
| `PLAN.md` | The original plan, feature list and test checklist |

## AI tools used

Built with Claude Code (Claude Opus 5), which was used to write the database
models, the authentication and task routes, and the Jinja2 templates, and to run
the test checklist in `PLAN.md` section 8.

## Known trade-offs

This is a learning project, and two security shortcuts were taken knowingly. Both
should be fixed before this is exposed to real users on a real network.

**Logout is a GET request.** `/logout` responds to a normal link click, so any
page a logged-in user visits could end their session by embedding something like
`<img src="http://127.0.0.1:5000/logout">`. This is accepted for now because the
worst outcome is a nuisance — the user is logged out and logs back in. No data is
read, changed or destroyed. The proper fix is to make logout a POST form with a
CSRF token, which is the same piece of work as the item below.

**There is no CSRF protection on the forms.** Signup, login, add, edit, delete and
toggle all accept a POST without a token, so a malicious page could submit one on
behalf of a logged-in user and, for example, delete a task. This is accepted
because the standard fix is Flask-WTF, and the project brief limits dependencies
to what is already in `requirements.txt`. Two things limit the damage in the
meantime: the destructive routes (`delete`, `toggle`) refuse GET and return 405,
so they cannot be triggered by an image tag or a plain link; and every route that
touches a single task first checks that the task belongs to the logged-in user,
so an attacker can only ever affect the victim's own rows, never anyone else's.
