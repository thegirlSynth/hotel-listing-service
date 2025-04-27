# 🚀 Project Setup Guide

This document will guide you through setting up this project on your local machine.

---

## 📦 Prerequisites

Make sure you have the following installed:
- [Python 3.10+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Git](https://git-scm.com/)

---

## 🛠️ Local Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/thegirlSynth/bettarest-backend.git
cd bettarest-backend
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

---

### 3. Activate the virtual environment

- **On Windows:**
  ```bash
  .\venv\Scripts\activate
  ```
- **On macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

---

### 4. Install project dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Create a `.env` file

Create a `.env` file in the root directory of the project, and add the following:

```bash
# .env file (example)

# Database connection URL for SQLAlchemy
# Format: postgresql+psycopg2://<username>:<password>@<host>/<database_name>
DATABASE_URL=postgresql+psycopg2://username:password@localhost/your_database_name

# Secret key used to sign JWT tokens
SECRET_KEY=your-secret-key

# Algorithm used for encoding JWT tokens (commonly HS256)
ALGORITHM=HS256

# Access token expiry time in minutes (e.g., 60 minutes = 1 hour)
ACCESS_TOKEN_EXPIRE_MINUTES=60

```

>  Ensure that the `DATABASE_URL` points to your local or remote database.

---

### 6. Run Alembic migrations

Make sure that the database specified in `DATABASE_URL` exists, and is running.

Run the following command to apply the existing database migrations to create the tables:

```bash
alembic upgrade head
```

---

### 7. Create a superuser

Before running the application, you'll need to create a superuser with owner privileges.

Run the following command to create the superuser:

```bash
python -m app.db.init_db
```

---

### 8. Start the application

Make sure you are in the **project root directory**, then start the server:

```bash
uvicorn app.main:app --reload
```

- The app should now be running at:
   http://127.0.0.1:8000

---

### 9. Access API Documentation
FastAPI automatically generates API documentation for your project. Once the server is running, you can access the documentation at:

  - Swagger UI: http://127.0.0.1:8000/docs

  - ReDoc UI: http://127.0.0.1:8000/redoc

---

### 10. Testing the Endpoints
You can test API endpoints using tools like Postman, Insomnia, or directly through the Swagger UI.

---

### 11. Example Routes
  * `POST /users/register`: Register a new user.

  * `POST /users/login`: Login and get a JWT token.

  * `PATCH /users/{user_id}/role`: Owner can update the roles of users (staff, admin, owner).

---

## 💬 Useful Commands

- Deactivate virtual environment:
  ```bash
  deactivate
  ```

- Install new package & update requirements.txt:
  ```bash
  pip install package-name
  pip freeze > requirements.txt
  ```

---

## 🧹 Troubleshooting

- **Issue:** Can't connect to database

  **Solution:** Double-check your `DATABASE_URL` in `.env`, and confirm your Postgres server is running.

- **Issue:** Migration error

  **Solution:** Make sure you ran `alembic upgrade head` after setting up the `.env` file.

---

