# HolbyDoc Installation and Usage Guide

## Prerequisites
- Python 3.11
- pip (Python package manager)
- Git (to clone the repository)

## Installation

1. Clone the repository:
```bash
git clone <repository_url>
cd HolbyDoc
```

2. Create a Python virtual environment:
```bash
python3.11 -m venv venv
```

3. Activate the virtual environment:
- On Linux/Mac:
```bash
source venv/bin/activate
```
- On Windows:
```bash
.\venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create the database:
```bash
python create_db.py
```

## Configuration

1. Environment variables (optional):
- Create a `.env` file at the project root
- Add the necessary variables:
```
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///holbydoc.db
```

## Launching the Application

1. Start the development server:
```bash
python run.py
```

2. Access the application:
- Open a web browser
- Go to: http://localhost:5000

## Usage

### Creating an Account
1. Click "Register" in the navigation bar
2. Fill out the form with:
   - First name
   - Last name
   - Username
   - Email
   - Password (minimum 8 characters, with uppercase, lowercase, numbers, and special characters)

### Creating a Course
1. Log in to your account
2. Go to "Dashboard"
3. Click "New Course"
4. Fill in the course information:
   - Title
   - Description
   - Icon (jpg or png format)

### Creating a Lesson
1. Log in to your account
2. Go to "Dashboard"
3. Select "New Lesson"
4. Fill in the information:
   - Select the course
   - Lesson title
   - Slug (URL-friendly)
   - Content (using CKEditor)
   - Cover image

## Features

- Complete authentication system
- Course and lesson management
- Rich text editor (CKEditor)
- Image file system
- Responsive interface

## Common Troubleshooting

1. Database error:
   - Verify that `create_db.py` has been executed
   - Check folder permissions

2. Dependency installation issues:
   - Check Python version (3.11 recommended)
   - Update pip: `pip install --upgrade pip`

3. Image upload problems:
   - Check permissions of the static/user_pics folder
   - Verify the format is jpg or png

## Support

For any questions or issues, you can:
1. Open an issue on GitHub
2. Contact the development team
3. Consult the technical documentation in the Holberton_report/ folder

## Security

- Never share your SECRET_KEY
- Use strong passwords
- Regularly update dependencies
- Pay attention to file permissions