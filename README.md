<div align="center">

# 🎓 Smart Class Attendance Calculator

### A Full-Stack Attendance Management System built with Python, Flask, Streamlit & PostgreSQL

Track attendance • Manage subjects • Analyze performance • Calculate safe bunks • Multi-user support

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge&logo=streamlit)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql)
![REST API](https://img.shields.io/badge/REST-API-green?style=for-the-badge)
![GitHub](https://img.shields.io/badge/Open%20Source-Project-success?style=for-the-badge)

</div>

---

# 📖 Overview

Smart Class Attendance Calculator is a **full-stack attendance management system** developed for students to efficiently manage attendance records, monitor attendance percentage, calculate safe bunks, and visualize attendance statistics through an interactive dashboard.

The application follows a **REST API architecture** where the frontend is built using **Streamlit**, the backend uses **Flask**, and **PostgreSQL** stores all user, subject, and attendance information.

---

# ✨ Features

## 🔐 Authentication

- User Registration
- Secure Login
- Session Management
- Logout
- Multi-user Support

---

## 📚 Subject Management

- Add Subject
- Edit Subject
- Delete Subject
- Subject Code Validation
- Target Attendance Management
- Duplicate Subject Detection

---

## 📝 Attendance Management

- Mark Attendance
- Select Attendance Date
- Present / Absent Status
- Edit Attendance Record
- Delete Attendance Record
- Delete Confirmation
- Attendance History
- Attendance Filters
- Live Attendance Summary

---

## 📊 Dashboard

- Total Subjects
- Overall Attendance
- Present Classes
- Absent Classes
- Safe Bunks
- Warning Subjects
- Recent Attendance Activity
- Subject Overview
- Progress Bar
- Attendance Distribution

---

## 📈 Analytics

- Overall Attendance Analysis
- Subject-wise Performance
- Attendance Distribution
- Attendance Trends
- Performance Insights

---

## 👤 Profile

- User Information
- Attendance Statistics
- Account Details

---

# 🏗️ System Architecture

```text
                Streamlit Frontend
                        │
                        │ HTTP Requests
                        ▼
                Flask REST API
                        │
                        ▼
                 PostgreSQL Database
```

---

# 🗄️ Database Design

```text
Users
│
├──────── Subjects
│             │
│             └──────── Attendance
```

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Frontend | Streamlit |
| Backend | Flask |
| Database | PostgreSQL |
| Language | Python |
| Charts | Plotly |
| Data Processing | Pandas |
| Database Driver | Psycopg2 |
| API Communication | Requests |

---

# 📂 Project Structure

```text
Smart-Class-Attendance-Calculator/

│
├── backend/
│   │
│   ├── app.py
│   ├── db.py
│   ├── routes/
│   ├── api_routes/
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── app.py
│   ├── pages/
│   ├── components/
│   ├── data/
│   └── assets/
│
├── database/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Smart-Class-Attendance-Calculator.git

cd Smart-Class-Attendance-Calculator
```

---

## Create Virtual Environment

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

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure PostgreSQL

Create a PostgreSQL database.

Update your database credentials inside:

```text
backend/db.py
```

---

## Start Backend

```bash
cd backend

python app.py
```

---

## Start Frontend

Open another terminal.

```bash
cd frontend

streamlit run app.py
```

---

# 📷 Application Screenshots

> Replace these with your screenshots.

| Login | Dashboard |
|-------|-----------|
| ![](assets/login.png) | ![](assets/dashboard.png) |

| Subjects | Attendance |
|----------|------------|
| ![](assets/subjects.png) | ![](assets/attendance.png) |

| Analytics | Profile |
|-----------|---------|
| ![](assets/analytics.png) | ![](assets/profile.png) |

---

# 🎯 Project Highlights

- REST API Based Architecture
- PostgreSQL Database Integration
- Multi-user Support
- Secure Authentication
- Attendance Tracking
- Subject Management
- Attendance Analytics
- Dashboard Visualization
- Safe Bunks Calculator
- Warning Detection
- Interactive Charts
- CRUD Operations

---

# 💻 Skills Demonstrated

- Python Programming
- Flask Development
- Streamlit Development
- PostgreSQL
- SQL
- REST APIs
- CRUD Operations
- Database Design
- Data Visualization
- Dashboard Development
- Git
- GitHub

---

# 🔮 Future Enhancements

- Email-based Password Reset
- Email Notifications
- CSV / Excel Export
- Calendar View
- Mobile Responsive UI
- Admin Panel
- Cloud Deployment
- Docker Support

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push your branch
5. Create a Pull Request

---

# 📄 License

This project is developed for educational and learning purposes.

---

# 👨‍💻 Developer

**Shreyansh Kumar**

B.Tech Computer Science & Engineering

Lovely Professional University

GitHub:
https://github.com/YOUR_USERNAME

---

<div align="center">

### ⭐ If you found this project useful, don't forget to star the repository!

Made with ❤️ using Python, Flask, Streamlit & PostgreSQL

</div>