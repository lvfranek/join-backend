# Join Backend

> **This is the backend repository.** The user interface lives in the frontend repository:
> **[lvfranek/Join](https://github.com/lvfranek/Join)** (Angular).
> This API is meant to be used together with that app.

REST API for **Join**, a Kanban-style task manager. It handles user accounts, contacts and tasks, and makes sure every user only sees their own data. Built with Django and Django REST Framework.

## Table of Contents

- [Tech Stack](#tech-stack)
- [Features](#features)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Data Model](#data-model)
- [Deployment](#deployment)

## Tech Stack

- `Python` 3.14
- `Django` 6.1
- `Django REST Framework` 3.18 with token authentication
- `django-cors-headers` to allow requests from the Angular app
- `python-dotenv` for configuration via `.env`
- `SQLite` as the database

## Features

- **Registration and login** with email and password. Passwords are stored hashed.
- **Token authentication**: login returns a token that the frontend sends with every request. Logout deletes the token on the server.
- **Contacts and tasks** with full create, read, update and delete support.
- **Data isolation**: every contact and task belongs to the user who created it. Users can only read, change or delete their own data. Requests for another user's objects return `404`.
- **Validation**: task status and priority only accept known values, and the assignee and subtask lists are checked for the right shape.
- **Django admin** to inspect and edit all data.

## Installation

**Prerequisites:** Python 3.12+ and Git.

1. Clone the repository:

   ```bash
   git clone https://github.com/lvfranek/join-backend.git
   cd join-backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows use `.venv\Scripts\activate`.

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create your environment file and set a secret key:

   ```bash
   cp .env.example .env
   ```

   Generate a key and paste it as `SECRET_KEY` in `.env`:

   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. Create the database tables:

   ```bash
   python manage.py migrate
   ```

6. Optional: create an admin user for the Django admin at `/admin/`:

   ```bash
   python manage.py createsuperuser
   ```

7. Start the server:

   ```bash
   python manage.py runserver
   ```

   The API now runs on `http://127.0.0.1:8000/api/`. Next, start the [frontend](https://github.com/lvfranek/Join#️-installation).

## Environment Variables

All variables live in `.env` in the project root (see `.env.example`).

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key. Required. | a long random string |
| `DEBUG` | `True` for local development, `False` in production | `True` |
| `ALLOWED_HOSTS` | Comma-separated host names the server answers to | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | Comma-separated origins allowed to call the API (the frontend URL) | `http://localhost:4200,http://127.0.0.1:4200` |

## API Endpoints

All endpoints except registration and login need the header `Authorization: Token <token>`.

**Auth**

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/registration/` | Create an account (`full_name`, `email`, `password`, `repeated_password`) |
| `POST` | `/api/auth/login/` | Log in with `email` and `password`, returns a token |
| `POST` | `/api/auth/logout/` | Delete the current token |
| `GET` | `/api/auth/me/` | Get the user the token belongs to |

Registration and login return:

```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user_id": 2,
  "email": "max@test.de",
  "full_name": "Max Muster"
}
```

**Contacts**

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/contacts/` | List your contacts |
| `POST` | `/api/contacts/` | Create a contact |
| `GET` | `/api/contacts/<id>/` | Get one contact |
| `PUT` / `PATCH` | `/api/contacts/<id>/` | Update a contact |
| `DELETE` | `/api/contacts/<id>/` | Delete a contact |

**Tasks**

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/tasks/` | List your tasks |
| `POST` | `/api/tasks/` | Create a task |
| `GET` | `/api/tasks/<id>/` | Get one task |
| `PUT` / `PATCH` | `/api/tasks/<id>/` | Update a task (the board uses `PATCH` when a card is moved) |
| `DELETE` | `/api/tasks/<id>/` | Delete a task |

Example task:

```json
{
  "id": 1,
  "title": "Build login page",
  "description": "Form with email and password",
  "status": "todo",
  "priority": "urgent",
  "dueDate": "2026-10-15",
  "category": "Technical Task",
  "assignees": [{ "id": "1", "name": "Anna Schmidt", "initials": "AS", "color": "#ff7a00" }],
  "subtasks": ["Create form", "Connect to API"]
}
```

With `DEBUG=True` you can also open every endpoint in the browser and use the browsable API of Django REST Framework (log in at `/admin/` first).

## Project Structure

```
join-backend/
├── core/             # Project settings and root URLs
├── user_auth_app/    # Registration, login, logout, current user
├── contacts_app/     # Contact model and API
├── tasks_app/        # Task model and API
└── manage.py
```

Each app keeps its API code in an `api/` folder with `serializers.py`, `views.py` and `urls.py`.

## Data Model

- **User**: Django's built-in user. The email is used as the username, the full name is stored in `first_name`.
- **Contact**: `first_name`, `last_name`, `email`, `phone`, `created_by` (user).
- **Task**: `title`, `description`, `status` (`todo`, `inProgress`, `awaitFeedback`, `done`), `priority` (`urgent`, `medium`, `low`), `due_date`, `category`, `assignees` (JSON list), `subtasks` (JSON list), `created_by` (user).

Deleting a user also deletes their contacts and tasks.

## Deployment

The API runs with Gunicorn behind Nginx on a Google Cloud VM, at `https://join-api.franekkaminski.dev`. In production, set `DEBUG=False` and point `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS` at the real domains.
