# 🚀 Smart Class Attendance Calculator Setup Guide

This guide explains how to run the project locally.

---

# 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Smart-Class-Attendance-Calculator.git

cd Smart-Class-Attendance-Calculator
```

---

# 2. Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Install PostgreSQL

Download PostgreSQL

https://www.postgresql.org/download/

Create a database.

Example:

```
attendance_db
```

---

# 5. Update Database Credentials

Open

```
backend/db.py
```

Update:

```python
host="localhost"
database="attendance_db"
user="postgres"
password="YOUR_PASSWORD"
port="5432"
```

---

# 6. Create Tables

Run your SQL schema inside PostgreSQL.

Tables required

- users
- subjects
- attendance

---

# 7. Run Backend

```bash
cd backend

python app.py
```

Backend runs at

```
http://127.0.0.1:5000
```

---

# 8. Run Frontend

Open another terminal

```bash
cd frontend

streamlit run app.py
```

Frontend runs at

```
http://localhost:8501
```

---

# 9. Login

Register a new account.

Add subjects.

Mark attendance.

Enjoy 🎉

---

# Folder Structure

```
backend/
frontend/
database/
README.md
SETUP.md
requirements.txt
```

---

# Tech Stack

- Python
- Flask
- Streamlit
- PostgreSQL
- Pandas
- Plotly