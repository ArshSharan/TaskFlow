# 🚀 Django MariaDB Task Manager

A modern, full-featured task management web application built with Django, MariaDB, and a beautiful interactive frontend. Organize your tasks, track progress, and boost your productivity—all with secure user authentication.

---

## ✨ Features

- 📝 **Task CRUD**: Create, read, update, and delete your personal tasks
- 🔒 **User Authentication**: Secure signup, login, and logout
- 🎨 **Modern UI**: Responsive, card-based design with color-coded statuses
- ⚡ **Real-time Interactions**: Add, update, and delete tasks without page reloads
- 🗃️ **MariaDB Integration**: Robust, scalable relational database
- 🔗 **RESTful API**: Easily integrate or extend with other services

---

## 🛠️ Tech Stack

- **Backend**: Django 5.x, Django REST Framework
- **Database**: MariaDB
- **Frontend**: HTML5, CSS3, JavaScript (vanilla), Font Awesome, Google Fonts

---

## 🚦 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Django-MariaDB-App
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```
DB_NAME=taskmanager
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 5. Create the Database in MariaDB
```sql
CREATE DATABASE taskmanager;
```

### 6. Run Migrations
```bash
python manage.py migrate
```

### 7. Create a Superuser (Optional, for admin access)
```bash
python manage.py createsuperuser
```

### 8. Start the Development Server
```bash
python manage.py runserver
```

Visit [http://localhost:8000/](http://localhost:8000/) in your browser.

---

## 🔑 Authentication
- Sign up for a new account or log in with existing credentials.
- Each user sees only their own tasks.
- Secure logout button in the header.

---

## 📦 API Endpoints

| Method | Endpoint         | Description                |
|--------|------------------|----------------------------|
| GET    | `/api/tasks/`    | List all tasks (user only) |
| POST   | `/api/tasks/`    | Create a new task          |
| GET    | `/api/tasks/<id>/` | Retrieve a task           |
| PUT    | `/api/tasks/<id>/` | Update a task             |
| DELETE | `/api/tasks/<id>/` | Delete a task             |

All endpoints require authentication.

---

## 🖼️ Screenshots

> _Add screenshots of your app here!_

---

## 🤝 Contributing

1. Fork this repo
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 💡 Credits

- Built with [Django](https://www.djangoproject.com/) and [MariaDB](https://mariadb.org/)
- UI inspired by modern productivity tools