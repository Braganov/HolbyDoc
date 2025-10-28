# 📚 HolbyDoc

> **Centralized educational platform for Holberton School**  
> A complete solution for managing and sharing educational resources

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📋 Table of Contents

- [About](#-about)
- [Project Context](#-project-context)
- [Features](#-features)
- [Technical Architecture](#-technical-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Security](#-security)
- [Deployment](#-deployment)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Author](#-author)
- [License](#-license)

---

## 🎯 About

**HolbyDoc** is a full-stack web platform developed to centralize and organize learning resources for Holberton School students. In response to the fragmentation of educational information, HolbyDoc offers a structured environment where users can access organized courses, create enriched content, and share their knowledge.

### Problem Solved

Holberton School students face:
- Scattered documentation across official platforms, external resources, and informal exchanges
- Advanced technical concepts requiring tailored explanations
- A need for centralization to optimize learning in an intensive program

HolbyDoc addresses these challenges by providing a unified, intuitive, and collaborative platform.

---

## 🌍 Project Context

This project was developed as part of the **RNCP5 "Web and Mobile Web Developer"** professional certification and demonstrates complete mastery of full-stack development:

- ✅ **Frontend**: Responsive interface with HTML5, CSS3, Bootstrap 5
- ✅ **Backend**: MVC architecture with Flask and blueprints
- ✅ **Database**: Relational modeling with SQLAlchemy
- ✅ **Security**: Flask-Login authentication, CSRF protection, Bcrypt hashing
- ✅ **Deployment**: Linux infrastructure with Nginx and Gunicorn

---

## ✨ Features

### 👤 User Management
- Secure registration and authentication
- Profile management with photo upload
- Role system (user, contributor, administrator)
- Password recovery

### 📖 Educational Content Management
- Course creation and organization by topics
- Detailed lessons with enriched content
- Integrated WYSIWYG editor (CKEditor)
- Image and media upload and management
- Intuitive hierarchical navigation

### 🔒 Advanced Security
- Password hashing with Bcrypt
- CSRF protection on all forms
- Server-side data validation
- HTML content sanitization
- Secure sessions with Flask-Login

### 🎨 User Interface
- Responsive design adapted to all devices
- Intuitive navigation with breadcrumbs
- Personalized dashboard for each user
- Flash messages for user feedback

---

## 🏗️ Technical Architecture

### Technology Stack

**Backend**
- Python 3.11
- Flask 2.0.3 (web framework)
- SQLAlchemy (ORM)
- Flask-Login (authentication)
- Flask-WTF (forms and CSRF)
- Flask-Bcrypt (password hashing)
- Flask-CKEditor (content editor)

**Frontend**
- HTML5 & CSS3
- Bootstrap 5.1.3
- Bootstrap Icons 1.8.1
- JavaScript
- Jinja2 (templates)

**Database**
- SQLite (development)
- PostgreSQL (production)

**Infrastructure**
- Nginx (reverse proxy)
- Gunicorn (WSGI server)
- Let's Encrypt (SSL certificates)

### MVC Architecture

```
┌─────────────────┐
│      User       │
└────────┬────────┘
         │
    ┌────▼────┐
    │  Nginx  │  ← Reverse proxy & static files
    └────┬────┘
         │
   ┌─────▼──────┐
   │  Gunicorn  │  ← WSGI server
   └─────┬──────┘
         │
   ┌─────▼──────┐
   │   Flask    │  ← Application (MVC)
   └─────┬──────┘
         │
   ┌─────▼──────┐
   │ PostgreSQL │  ← Database
   └────────────┘
```

---

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git
- Python virtual environment

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/Braganov/HolbyDoc.git
cd HolbyDoc
```

2. **Create and activate virtual environment**
```bash
python3.11 -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
.\venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Create a .env file at the root
echo "SECRET_KEY=your_very_long_secret_key" > .env
echo "SQLALCHEMY_DATABASE_URI=sqlite:///holbydoc.db" >> .env
```

5. **Initialize the database**
```bash
python create_db.py
```

6. **Launch the application**
```bash
python run.py
```

7. **Access the application**
Open your browser: `http://localhost:5000`

---

## 📖 Usage

### Registration
1. Click "Register" in the navigation bar
2. Fill out the form with your information
3. Validate to create your account

### Login
1. Click "Login"
2. Enter email and password
3. Access your personalized dashboard

### Create a Course
1. Log in to your account
2. Go to "Dashboard"
3. Click "New Course"
4. Fill in the information (title, description, icon)

### Create a Lesson
1. Select a course
2. Click "New Lesson"
3. Use the CKEditor to create enriched content
4. Add a cover image
5. Publish

---

## 📂 Project Structure

```
HolbyDoc/
│
├── holbydoc/                    # Main package
│   ├── __init__.py             # Application factory
│   ├── config.py               # Configuration
│   ├── models.py               # SQLAlchemy models
│   ├── forms.py                # WTForms forms
│   ├── helpers.py              # Utility functions
│   │
│   ├── main/                   # Main blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── users/                  # Users blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── helpers.py
│   │
│   ├── courses/                # Courses blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   │
│   ├── lessons/                # Lessons blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── helpers.py
│   │
│   ├── errors/                 # Error handling
│   │   ├── __init__.py
│   │   └── handlers.py
│   │
│   ├── static/                 # Static files
│   │   ├── main.css
│   │   ├── ckeditor/
│   │   ├── course_icons/
│   │   ├── lesson_thumbnails/
│   │   └── user_pics/
│   │
│   └── templates/              # Jinja2 templates
│       ├── layout.html
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       ├── dashboard.html
│       ├── course.html
│       ├── lesson.html
│       └── errors/
│
├── Holberton_report/           # Technical documentation
├── venv/                       # Virtual environment
├── create_db.py                # DB initialization script
├── run.py                      # Entry point
├── requirements.txt            # Python dependencies
├── GUIDE.md                    # Detailed usage guide
└── README.md                   # This file
```

---

## 🔒 Security

HolbyDoc implements several essential security measures:

### Authentication
- Password hashing with **Bcrypt** and unique salt
- Secure sessions with **Flask-Login**
- Cookies with `HttpOnly` and `Secure` flags
- Secure password recovery system

### Data Protection
- **CSRF protection** on all forms
- **Server-side data validation** with WTForms
- **Automatic escaping** of content with Jinja2
- **HTML sanitization** for CKEditor content

### Attack Prevention
- Protection against **SQL injections** via SQLAlchemy ORM
- Protection against **XSS attacks** (Cross-Site Scripting)
- **Secure upload** with MIME type validation
- Environment variables for **secrets**

### Access Control
- **Role system** (user, contributor, admin)
- `@login_required` decorators for protected routes
- **Permission verification** before modification

---

## 🌐 Deployment

### Production Configuration

1. **Linux Server** (Ubuntu recommended)
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv nginx postgresql
```

2. **PostgreSQL Configuration**
```bash
sudo -u postgres createdb holbydoc
sudo -u postgres createuser holbydoc_user
```

3. **Gunicorn Installation**
```bash
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:8000 run:app
```

4. **Nginx Configuration**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/holbydoc/holbydoc/static;
    }
}
```

5. **SSL Certificate with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

For more details, see [GUIDE.md](GUIDE.md).

---

## 🗺️ Roadmap

### Short Term
- [ ] Advanced search system with filters
- [ ] Discussion space (comments under lessons)
- [ ] Favorites and personalized learning paths

### Medium Term
- [ ] REST API for third-party integrations
- [ ] Mobile application (PWA)
- [ ] Real-time notifications

### Long Term
- [ ] Quiz and assessment system
- [ ] AI for content recommendations
- [ ] Multilingual support
- [ ] Integrated community forum

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards
- Follow **PEP 8** conventions for Python
- Document functions with docstrings
- Add tests for new features
- Update documentation as needed

---

## 👨‍💻 Author

**Ibrahim Houmaidi**
- Education: Holberton School Paris - Cohort C17 (2023-2024)
- Certification: RNCP5 "Web and Mobile Web Developer"
- GitHub: [@Braganov](https://github.com/Braganov)
- Email: ibrahim.houmaidi@example.com

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Holberton School** for training and support
- The **Flask** community for documentation and resources
- All **students** who tested and provided feedback
- Open source **contributors** of the libraries used

---

## 📚 Additional Documentation

- [Detailed installation guide](GUIDE.md)
- [Technical documentation](Holberton_report/)
- [Screenshots](Holberton_report/screenshots/)
- [UML diagrams](Holberton_report/diagrams/)

---

## 🌟 Support

If you find this project useful, feel free to:
- ⭐ Star on GitHub
- 🐛 Report bugs via Issues
- 💡 Suggest improvements
- 📢 Share with other students

---

**Made with ❤️ for the Holberton School community**

*[View English version](./README.md) | [Voir la version française](./README_FR.md)*
