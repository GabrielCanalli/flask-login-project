# flask-login-project
Flask login system (under development)

# 🔐 Flask Authentication System (ADS Project)
This is a complete full-stack authentication system, developed as a practical project for the **Systems Analysis and Development (ADS)** degree program. The project implements the fundamental concepts of web development, relational database persistence, and session management.

## 🚀 Overview
The application provides a solid foundation for user management, featuring a modern **Dark Mode** interface. The project demonstrates the integration of a Python backend with a database to handle user registration, secure login, and route protection logic.
The application provides a solid foundation for user management, featuring a modern **Dark Mode** interface. The project demonstrates the integration of a Python backend with a database to handle user registration, secure login, and route protection logic.

## 🛠️ Technologies Used
* **Backend:** [Python](https://www.python.org/) with [Flask](https://flask.palletsprojects.com/) (Micro-Framework)
* **Database:** [SQLite3](https://www.sqlite.org/index.html) (Relational Data Management)
* **Frontend:** HTML5 and CSS3 (Custom Interface)
* **Sessions:** Flask-Session for secure user state persistence.

## ✨ Main Features
* **User Registration:** Real-time validation to prevent duplicate usernames using SQL **UNIQUE** constraints.
* **Secure Login:** Credential verification directly against the SQLite database.
* **Protected Dashboard:** Routes accessible only to authenticated users through session verification.
* **Flash Messages:** Dynamic visual alerts for successful or failed actions (e.g., "Access Denied", "Welcome").
* **Data Persistence:** Information is stored in a local `.db` file, ensuring that data is not lost when the server restarts.

## 📂 Project Structure
```text
flask-login-project/
├── app.py              # Main application logic and database configuration
├── database.db         # SQLite database file (generated automatically)
├── static/
│   └── css/
│       └── style.css   # Dark Mode styling and layout
└── templates/          # HTML templates with Jinja2
    ├── login.html      # Login interface
    ├── register.html   # Registration interface
    └── dashboard.html  # Restricted user area
```
---
### 👤 Author
**Gabriel Canalli**  
*Systems Analysis and Development Student (3rd Semester)*
