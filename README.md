# TaskFlow - Modern Task Management

A sleek, full-featured task management web application built with **Django**, **TiDB Cloud**, and a beautiful interactive frontend. Organize your tasks, track progress, and boost your productivity with secure cloud-based data storage.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://djangoproject.com)
[![TiDB](https://img.shields.io/badge/Database-TiDB%20Cloud-orange.svg)](https://tidbcloud.com)
[![Deploy](https://img.shields.io/badge/Deploy-Render-purple.svg)](https://render.com)

---

## Features

### Task Management
- **Full CRUD Operations**: Create, read, update, and delete tasks seamlessly
- **Categories & Priorities**: Organize tasks with custom categories and priority levels
- **Due Dates**: Set and track task deadlines
- **Status Tracking**: Monitor task progress (Pending, In Progress, Completed)

### User Experience
- **Secure Authentication**: User registration, login, and profile management
- **Personal Profiles**: Upload profile photos and manage user information
- **Real-time Updates**: Dynamic task updates without page reloads
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices

### Modern Interface
- **Beautiful UI**: Card-based design with intuitive color coding
- **Interactive Elements**: Smooth animations and hover effects
- **Dashboard Analytics**: Task statistics and progress visualization
- **Quick Actions**: Fast task creation and management shortcuts

---

## Tech Stack

### Backend
- **Framework**: Django 5.2.3
- **API**: Django REST Framework 3.14.0
- **Database**: TiDB Cloud (MySQL-compatible)
- **Authentication**: Django built-in auth with custom user profiles

### Frontend
- **HTML5** with modern semantic markup
- **CSS3** with Flexbox/Grid layouts
- **JavaScript** (ES6+) for dynamic interactions
- **Font Awesome** for icons
- **Google Fonts** (Inter) for typography

### Infrastructure
- **Hosting**: Render.com
- **Database**: TiDB Cloud (free tier)
- **SSL/TLS**: Automated HTTPS
- **Static Files**: WhiteNoise + CDN

---

## Quick Start

### Prerequisites
- Python 3.8+
- Git
- TiDB Cloud account (free)

### 1. Clone the Repository
```bash
git clone https://github.com/ArshSharan/TaskFlow.git
cd TaskFlow
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# TiDB Cloud Database Configuration
DB_NAME=your-database-name
DB_USER=your-tidb-username
DB_PASSWORD=your-tidb-password
DB_HOST=gateway01.ap-southeast-1.prod.aws.tidbcloud.com
DB_PORT=4000
DB_SSL_CA=./certs/ca-cert.pem
```

### 5. Set Up TiDB Cloud Database
1. Sign up at [TiDB Cloud](https://tidbcloud.com)
2. Create a new cluster (free tier available)
3. Download the SSL certificate to `certs/` folder
4. Update your `.env` with connection details

### 6. Run Database Migrations
```bash
python manage.py migrate
```

### 7. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 8. Start Development Server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** to start using TaskFlow!

---

## Live Demo

Check out the live application: **[TaskFlow on Render](https://taskflow-wrw6.onrender.com/)**

---
## 🔗 API Documentation

### Authentication Required
All API endpoints require user authentication via Django sessions.

### Task Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/tasks/` | List user's tasks |
| `POST` | `/api/tasks/` | Create new task |
| `GET` | `/api/tasks/{id}/` | Get specific task |
| `PUT` | `/api/tasks/{id}/` | Update task |
| `DELETE` | `/api/tasks/{id}/` | Delete task |
| `GET` | `/api/tasks/dashboard_stats/` | Get dashboard statistics |

### Profile Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/profile/me/` | Get user profile |
| `PATCH` | `/api/profile/update_profile/` | Update profile |
| `POST` | `/api/profile/change_password/` | Change password |

### Quick Actions
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/quick-actions/` | Get user's quick actions |
| `POST` | `/api/quick-actions/` | Create quick action |

---
---

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**:
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to the branch**:
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed

---

## Future Prospects

- [ ] Email notifications for due dates
- [ ] Task templates and recurring tasks
- [ ] Team collaboration features
- [ ] Advanced analytics and reporting
- [ ] Mobile app (React Native)
- [ ] Third-party integrations (Calendar, Slack)

---

## Troubleshooting

### Common Issues

**Database Connection Error**:
```bash
# Check TiDB connection details in .env
# Ensure SSL certificate is in certs/ folder
```

**Static Files Not Loading**:
```bash
python manage.py collectstatic
```

**Migration Issues**:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **[Django](https://djangoproject.com)** - The web framework for perfectionists
- **[TiDB Cloud](https://tidbcloud.com)** - Scalable, cloud-native database
- **[Render](https://render.com)** - Simple cloud hosting
- **[Font Awesome](https://fontawesome.com)** - Beautiful icons
- **[Google Fonts](https://fonts.google.com)** - Typography

---

</div>
