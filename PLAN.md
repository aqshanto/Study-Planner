## PLAN -> Study Planner

## 1. Problem

- we are making a small web app based on study planner. we are using python flask, flask login, flask sqlalchemy for database, bootstrap 5 via CDN.

## 2. Users and Roles.

- Guests can : signup / login .
- Users can : add, edit, delete and filter their own tasks, and mark them done.

## 3. Must have Feature (From problem statement)

- [ ] User signup : Create a new account
- [ ] User login/logout : Manage user sessions
- [ ] Add task : Create a study task
- [ ] Edit task : Update task details
- [ ] Delete task : Remove a task
- [ ] Task details : Store title, subject, deadline, priority
- [ ] Task status : Mark task as pending or done
- [ ] User-specific tasks : Each user only sees their own tasks
- [ ] Task filtering : View pending or completed tasks
- [ ] Overdue highlighting : Show pending tasks whose deadline has passed

## 4. Nice to Have (only if time is left)

- [ ] Progress statistics : Show completed task percentage
- [ ] Calendar view : Display tasks by date

## 5. Databse Tables

User

- id: Integer, primary key
- username: String(80), required
- email: String(120), required, unique
- password_hash: String(255), required

Task

- id: Integer, primary key
- title: String(120), required
- subject: String(80)
- deadline: Date
- priority: String(10) # "low" | "medium" | "high"
- status : String(10) # "pending" | "done"
- user_id: Integer, ForeignKey → User.id, required

Relationship: one User has many Tasks; each Task belongs to exactly one User.

## 6. Routes

| URL                         | Method    | Purpose                                  | Access |
| --------------------------- | --------- | ---------------------------------------- | ------ |
| `/signup`                   | GET, POST | Display signup page and create account   | No     |
| `/login`                    | GET, POST | Display login page and authenticate user | No     |
| `/logout`                   | GET       | Logout current user                      | Yes    |
| `/dashboard`                | GET       | Required login                           | Yes    |
| `/dashboard?status=pending` | GET       | Show login page                          | Yes    |
| `/dashboard?status=done`    | GET       | Show user's task list                    | Yes    |
| `/task/add`                 | GET, POST | Create a new task                        | Yes    |
| `/task/<id>/edit`           | GET, POST | Edit an existing task                    | Yes    |
| `/task/<id>/delete`         | POST      | Delete a task                            | Yes    |
| `/task/<id>/toggle`         | POST      | Change pending/done status               | Yes    |

## 7. Build Order with times

## Phase 1: Project Setup (10 minutes)

### Tasks:

- Create Flask project structure
- Setup virtual environment
- Install required packages
- Connect SQLite database
- Configure Flask application

### Output:

- Flask app runs successfully
- Database connection is ready

---

## Phase 2: Database Design (15 minutes)

### Create Models:

### User Table

Fields:

- id
- username
- email
- password_hash

### Task Table

Fields:

- id
- title
- subject
- deadline
- priority
- status
- user_id

### Relationship:

User
|
| 1
|
|------ Many
|
Task

### Output:

- Database tables created
- User and Task relationship working

---

## Phase 3: Authentication System (25 minutes)

### Build:

### Signup

- Create new user account
- Store password securely

### Login

- Verify user credentials
- Create login session

### Logout

- End user session

### Route Protection:

- Only logged-in users can access planner pages

### Output:

- User can register
- User can login
- User can logout

---

## Phase 4: Task Dashboard (15 minutes)

### Build Main Page:

Display:

- Task title
- Subject
- Deadline
- Priority
- Status

Important:

- User can only see their own tasks

### Output:

- Personal task dashboard works

---

## Phase 5: Task CRUD Operations (30 minutes)

### Add Task (10 minutes)

Create task form:

Fields:

- Title
- Subject
- Deadline
- Priority

Save task into database.

---

### Edit Task (10 minutes)

Allow user to update:

- Title
- Subject
- Deadline
- Priority

---

### Delete Task (10 minutes)

Allow user to remove tasks.

---

### Output:

- User can create, update, and delete tasks

---

## Phase 6: Status and Filtering (15 minutes)

### Task Status:

Add:

- Pending
- Done

Allow users to change task status.

---

### Task Filtering:

Create filters:

- All Tasks
- Pending Tasks
- Done Tasks

### Output:

- User can manage task progress

---

## Phase 7: Overdue Highlighting (5 minutes)

Rule:

If:

- Deadline is before today's date
- Status is pending

Then:

- Highlight the task

### Output:

- Overdue tasks are visible

---

## Phase 8: Testing and Bug Fixing (5 minutes)

Check:

- Signup works
- Login works
- Logout works
- Add task works
- Edit task works
- Delete task works
- Status change works
- Filtering works
- User isolation works
- Overdue highlighting works

---

# Final Timeline

| Phase                 |                      Time |
| --------------------- | ------------------------: |
| Project Setup         |                10 minutes |
| Database Design       |                15 minutes |
| Authentication System |                25 minutes |
| Task Dashboard        |                15 minutes |
| Task CRUD Operations  |                30 minutes |
| Status and Filtering  |                15 minutes |
| Overdue Highlighting  |                 5 minutes |
| Testing               |                 5 minutes |
| **Total**             | **120 minutes (2 hours)** |

---

# Application Flow

User

↓

Signup / Login

↓

Dashboard

↓

Create Task

↓

Save in Database

↓

Display Tasks

↓

Update Status

↓

Filter Tasks

## 8. Test Checklist

- [ ] Logged out: /dashboard, /task/add redirect to login
- [ ] Signup with an existing email is rejected
- [ ] Password is not stored in plain text (check the .db or print the hash)
- [ ] User A cannot open, edit or delete User B's task (test with 2 accounts)
- [ ] Add task → appears on dashboard with correct subject, deadline, priority
- [ ] Edit task → form shows old values, saves new ones
- [ ] Delete task → gone from dashboard
- [ ] Toggle → pending becomes done and back
- [ ] Filter pending / done / all each show the right rows
- [ ] Past deadline + pending is highlighted; past deadline + done is not
- [ ] App starts from a fresh clone with the README steps
