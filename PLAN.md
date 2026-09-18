## PLAN -> Study Planner

## 1. Problem

- we are making a small web app based on study planner. we are using python flask, flask login, flask sqlalchemy for database, bootstrap 5 via CDN.

## 2. Users and Roles.

- Admin can : add , remove, update users and there information.
- Users can : create their profile, see there dashboard. add tasks.

## 3. Must have Feature (From problem statement)

- [] User signup : Create a new account
- [] User login/logout : Manage user sessions
- [] Add task : Create a study task
- [] Edit task : Update task details
- [] Delete task : Remove a task
- [] Task details : Store title, subject, deadline, priority
- [] Task status : Mark task as pending or done
- [] User-specific tasks : Each user only sees their own tasks
- [] Task filtering : View pending or completed tasks
- [] Overdue highlighting : Show pending tasks whose deadline has passed

## 4. Nice to Have (only if time is left)

- [] Task search : Quickly find tasks
- [] Categories/tags : Organize tasks better
- [] Notes section : Add extra details to tasks
- [] Reminder notifications : Alert before deadlines
- [] Progress statistics : Show completed task percentage
- [] Calendar view : Display tasks by date
- [] Profile page : Manage user information
- [] Dark mode : Change interface appearance

## 5. Databse Tables

1. users (id, name , email, password_hash, is_admin)
2. Task (id, title, subject, deadline, priority, status,user_id)

## 6. Routes

| URL                      | Method    | Purpose                                  | Login Required |
| ------------------------ | --------- | ---------------------------------------- | -------------- |
| `/signup`                | GET, POST | Display signup page and create account   | No             |
| `/login`                 | GET, POST | Display login page and authenticate user | No             |
| `/logout`                | GET       | Logout current user                      | Yes            |
| `/dashboard`             | GET       | Show user's task list                    | Yes            |
| `/task/add`              | GET, POST | Create a new task                        | Yes            |
| `/task/<id>/edit`        | GET, POST | Edit an existing task                    | Yes            |
| `/task/<id>/delete`      | POST      | Delete a task                            | Yes            |
| `/task/<id>/toggle`      | POST      | Change pending/done status               | Yes            |
| `/tasks/filter/<status>` | GET       | Filter tasks by status                   | Yes            |

## 7. Build Order with times

### Step 1: Setup Flask Project

Create:

Flask application
Template folder
Database connection
Bootstrap setup

Goal:
A basic Flask page should load.

### Step 2: Create Database Models

Create:

User table
Task table
User-task relationship

Goal:
Database structure is ready.

### Step 3: Add Authentication

Build:

Signup
Login
Logout

Goal:
Users can create accounts and access their own sessions.

### Step 4: Create Task Dashboard

Build:

Display logged-in user's tasks
Show empty task list initially

Goal:
User has a personal planner page.

### Step 5: Add Task CRUD

Add:

Create task
Read task list
Update task
Delete task

Goal:
Complete task management.

### Step 6: Add Status System

Add:

Pending status
Done status
Toggle button

Goal:
Users can track completion.

### Step 7: Add Filtering

Add:

View all tasks
View pending tasks
View completed tasks

Goal:
Make task management easier.

### Step 8: Add Overdue Highlighting

Add logic:

Deadline passed + pending status = overdue

Goal:
Important unfinished tasks are visible.

### Step 9: Final Testing

Check:

✅ User registration works
✅ Login/logout works
✅ Users only see their own tasks
✅ Tasks can be created, edited, deleted
✅ Status changes work
✅ Filters work
✅ Overdue tasks appear correctly

## 4. Test Checklist

1. User Authentication Testing

Signup

☐ User can open signup page
☐ User can create an account with valid information
☐ User cannot signup with missing required fields
☐ User cannot create duplicate account with same email/username
☐ Password is stored securely (not plain text)
☐ After signup, user can log in successfully

Login

☐ User can open login page
☐ User can login with correct credentials
☐ User cannot login with wrong password
☐ User cannot login with invalid email/username
☐ Error message appears for failed login
☐ Successful login redirects to dashboard

Logout

☐ Logged-in user can logout
☐ After logout, user cannot access protected pages
☐ User is redirected to login page after logout

2. Task Creation Testing
   
Add Task

☐ Logged-in user can open add task page
☐ User can create a task with all required fields

Check fields:

☐ Title saves correctly
☐ Subject saves correctly
☐ Deadline date saves correctly
☐ Priority saves correctly
☐ Default status is pending

☐ New task appears on dashboard after creation

3. Task Viewing Testing

Dashboard

☐ User can see their own tasks
☐ Empty dashboard works when user has no tasks
☐ Task information displays correctly:

☐ Title
☐ Subject
☐ Deadline
☐ Priority
☐ Status

4. User Data Protection Testing

User Isolation

Create two users:

User A
User B

Test:

☐ User A can see User A's tasks
☐ User A cannot see User B's tasks
☐ User B can see User B's tasks
☐ User B cannot edit User A's tasks
☐ User B cannot delete User A's tasks

5. Task Edit Testing

☐ User can open edit page
☐ Existing task data appears correctly
☐ User can update title
☐ User can update subject
☐ User can update deadline
☐ User can change priority
☐ Updated information appears on dashboard

6. Task Delete Testing

☐ User can delete their own task
☐ Deleted task disappears from dashboard
☐ Deleted task is removed from database
☐ User cannot delete another user's task

7. Task Status Testing

Mark Done

☐ Pending task can be marked as done
☐ Status changes from pending → done
☐ Done task displays correctly

Mark Pending

☐ Done task can be changed back to pending
☐ Status changes from done → pending

8. Task Filtering Testing

Pending Filter

☐ Pending filter button works
☐ Only pending tasks are displayed
☐ Done tasks are hidden

Done Filter

☐ Done filter button works
☐ Only completed tasks are displayed
☐ Pending tasks are hidden

All Tasks

☐ All tasks view shows both pending and done tasks

9. Deadline and Overdue Testing

Create tasks:

Past deadline + pending status
Future deadline + pending status
Past deadline + done status

Check:

☐ Past deadline pending task is highlighted
☐ Future deadline pending task is normal
☐ Completed overdue task is not highlighted

10. Access Control Testing

Without login:

☐ User cannot open dashboard
☐ User cannot add tasks
☐ User cannot edit tasks
☐ User cannot delete tasks

After login:

☐ All task features become available

11. UI Testing

☐ Navigation bar works
☐ Forms display correctly
☐ Buttons work properly
☐ Bootstrap styling loads
☐ Error messages are understandable
☐ Layout works on desktop and mobile

12. Final Project Acceptance Checklist

Before considering the project complete:

☐ Signup works
☐ Login works
☐ Logout works
☐ User-specific data works
☐ Add task works
☐ Edit task works
☐ Delete task works
☐ Status update works
☐ Filtering works
☐ Overdue highlighting works
☐ No user can access another user's tasks
☐ Database stores data correctly
☐ App runs without errors
