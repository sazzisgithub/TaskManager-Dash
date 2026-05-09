# TaskManager-Dashboard

A full-stack project management web application where teams can create projects, assign tasks, track progress, and collaborate with role-based access control.

🔗 **Live Demo:** [taskflow-frontend](https://taskmanager-frontend-eu8d.onrender.com/)  
🔗 **Backend API:** [taskflow-backend](https://taskmanager-dash-1.onrender.com)  
📁 **GitHub:** [https://github.com/sazzisgithub/TaskManager-Dash](https://github.com/sazzisgithub/TaskManager-Dash.git)

---

## Features

- **Authentication** — JWT-based signup/login; first user auto-assigned Admin role
- **Project Management** — Create, edit, archive projects with progress tracking
- **Task Management** — Tasks with priority, status, assignee and due date
- **Kanban Board** — View tasks across To Do → In Progress → Review → Done
- **Dashboard** — Live stats, overdue tasks, my tasks, recently updated
- **Comments** — Add comments on any task with timestamps
- **Role-Based Access** — System-level (Admin/Member) + per-project roles
- **Team View** — Admin can view all registered users

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.x + Django REST Framework |
| Auth | JWT via `djangorestframework-simplejwt` |
| Database | PostgreSQL (Render managed) |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Hosting | Render Web Service + Render Static Site |

---

## Project Structure

```
TaskManager-Dash/
├── Team_Task_Manager/       # Django backend
│   ├── apps/
│   │   ├── Users/           # Auth, custom user model
│   │   ├── Project/         # Project & member management
│   │   └── Tasks/           # Tasks, comments, dashboard
│   ├── manage.py
│   ├── requirements.txt
│   └── build.sh
└── Frontend/                # Static frontend
    ├── index.html
    ├── style.css
    ├── api.js
    ├── dashboard.js
    └── projects.js
```

---

## Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/TaskManager-Dash.git
cd TaskManager-Dash/Team_Task_Manager

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=taskflow_db
DB_USER=root
DB_PASSWORD=yourpassword

# 4. Run migrations and start server
python manage.py migrate
python manage.py runserver
```

Serve the frontend:
```bash
cd Frontend && python -m http.server 8080
# Open http://localhost:8080
```

---

## API Overview

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/signup/` | Register user |
| POST | `/api/auth/login/` | Login, returns JWT |
| GET | `/api/project/` | List projects |
| POST | `/api/project/` | Create project |
| GET | `/api/tasks/?project=1` | List tasks with filters |
| POST | `/api/tasks/` | Create task |
| PATCH | `/api/tasks/{id}/status/` | Update task status |
| POST | `/api/tasks/{id}/comment/` | Add comment |
| GET | `/api/tasks/dashboard/` | Dashboard stats |

---

## Role-Based Access

| Role | Access |
|---|---|
| **System Admin** | Full access to all projects, tasks, and users |
| **System Member** | Access only to assigned projects |
| **Project Admin** | Manage tasks and members within their project |
| **Project Member** | View tasks, update status, add comments |

---

## Author

SAJAL SHRIVASTAVA — Python Backend Developer  
Built as a full-stack assessment project demonstrating Django REST APIs, JWT auth, PostgreSQL, and role-based access control.
