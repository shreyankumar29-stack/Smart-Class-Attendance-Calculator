# ⚙️ Smart Class Attendance Calculator - Setup Guide

This guide explains how to install and run the Smart Class Attendance Calculator project on your local machine.

---

# 📋 Prerequisites

Make sure the following software is installed:

- Python 3.10 or above
- PostgreSQL
- Git
- Visual Studio Code (Recommended)

---

# 📥 Step 1: Clone Repository

```bash
git clone <your-github-repository-url>
cd Smart-Class-Attendance-Calculator
```

---

# 🐍 Step 2: Create Virtual Environment

Open terminal in the project folder and run:

```bash
python -m venv .venv
```

---

# ▶️ Step 3: Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux/Mac

```bash
source .venv/bin/activate
```

After activation, you should see:

```bash
(.venv)
```

in the terminal.

---

# 📦 Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

Verify installation:

```bash
pip list
```

---

# 🗄️ Step 5: Setup PostgreSQL Database

Open PostgreSQL and create a database:

```sql
CREATE DATABASE attendance_db;
```

Connect to the database:

```sql
\c attendance_db
```

---

# 📚 Step 6: Create Subjects Table

```sql
CREATE TABLE subjects(
    id SERIAL PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    subject_code VARCHAR(20) UNIQUE NOT NULL,
    target_percentage INTEGER DEFAULT 75
);
```

---

# 📅 Step 7: Create Attendance Table

```sql
CREATE TABLE attendance(
    id SERIAL PRIMARY KEY,
    subject_id INTEGER REFERENCES subjects(id)
    ON DELETE CASCADE,
    attendance_date DATE,
    status VARCHAR(20)
);
```

---

# ⚙️ Step 8: Configure Database Connection

Open:

```text
db.py
```

Update your PostgreSQL credentials:

```python
import psycopg2

def get_db_connection():

    return psycopg2.connect(
        host="localhost",
        database="attendance_db",
        user="postgres",
        password="YOUR_PASSWORD"
    )
```

Replace:

```text
YOUR_PASSWORD
```

with your PostgreSQL password.

---

# 🚀 Step 9: Run the Application

Run:

```bash
python app.py
```

If successful, you should see:

```bash
* Running on http://127.0.0.1:5000
```

---

# 🌐 Step 10: Open Browser

Open:

```text
http://127.0.0.1:5000/frontend
```

---

# 🧪 Testing Routes

### Home Route

```text
http://127.0.0.1:5000/
```

Expected:

```text
Smart Attendance Calculator Backend Running
```

### Dashboard

```text
http://127.0.0.1:5000/frontend
```

### Test Insert

```text
http://127.0.0.1:5000/test
```

---

# 📁 Project Structure

```text
Smart-Class-Attendance-Calculator/

├── routes/
├── templates/
├── static/
├── tests/
├── utils/
│
├── app.py
├── db.py
├── requirements.txt
├── README.md
├── SETUP.md
└── .gitignore
```

---

# ❗ Common Errors

### psycopg2 Error

Install:

```bash
pip install psycopg2-binary
```

---

### Flask Not Found

Install:

```bash
pip install flask
```

---

### Database Connection Error

Check:

- PostgreSQL service running
- Database name
- Username
- Password
- Port number

---

