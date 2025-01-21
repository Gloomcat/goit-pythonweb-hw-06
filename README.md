# Project README

## 📌 Setup with Poetry and Docker

### Prerequisites
Ensure you have **Poetry** and **Docker** installed.

### Install dependencies
```sh
poetry install
```

### Database setup
Run PostgreSQL container using Docker:
```sh
docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=1234 -d postgres
```

### Configure `.env` file (if required)
Ensure that your `.env` file contains the correct database connection settings.

---

## 🔹 Database Migration with Alembic
Alembic should be already initialized for project.

Generate initial migration:
```sh
poetry run alembic revision --autogenerate -m "Init"
```

Apply migrations:
```sh
poetry run alembic upgrade head
```

---

## ✅ Running Tests
Run seeding and selection tests using `pytest`:
```sh
poetry run pytest
```

---

## 📌 CLI Usage
The project provides a CLI for managing database records using `argparse`.

### 📌 Create a Teacher
```sh
poetry run python main.py -a create -m Teacher -n "Boris Jonson"
```

### 📌 List all Teachers
```sh
poetry run python main.py -a list -m Teacher
```

### 📌 Update a Teacher
```sh
poetry run python main.py -a update -m Teacher --id 3 -n "Andry Bezos"
```

### 📌 Remove a Teacher
```sh
poetry run python main.py -a remove -m Teacher --id 3
```

### 📌 Create a Group
```sh
poetry run python main.py -a create -m Group -n "AD-101"
```

### 📌 Create a Student with Foreign Key (Group)
```sh
poetry run python main.py -a create -m Student -n "Alice Brown" -gid 1
```

### 📌 Assign a Grade to a Student
```sh
poetry run python main.py -a create -m Grade -stid 1 -sid 2 -tid 3 -g 95
```

This CLI allows performing CRUD operations for **Teacher, Group, Student, Subject, and Grade** models.

---

## 🚀 Running the Application
Ensure the database is running before executing any commands:
```sh
docker ps  # Check if PostgreSQL is running
```

Run the main script:
```sh
poetry run main.py
```
