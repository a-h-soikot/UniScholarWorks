# UniScholarWorks – An Academic Thesis, Research Repository

UniScholarWorks is a full-stack web application built with the goal of streamlining the submission, tracking, review, and reading process of academic reports within a university environment. The platform supports dual-user roles (students and teachers) with role-based features, secure authentication, and document management.

---

## 🎬 Demo
[https://github.com/user-attachments/assets/e11c42c2-1c41-4289-820e-35f175784237](https://github.com/user-attachments/assets/fef38a51-75a8-4e2d-843c-55102585dae2)

---

## Key Features

👤 **User Management**
- Dual authentication system for students and faculty
- Secure OTP-based email verification for registration
- Session-based authentication with encrypted cookies
- Argon2 password hashing for enhanced security

📝 **Report Management**
- Submit research reports with metadata (title, authors, tags, summary)
- Browse and view submitted reports
- Generate AI-powered report summaries
- Tag-based organization and filtering

✅ **Review System**
- Teachers can review student submissions with detailed feedback
- Track pending reviews with dashboard notifications
- Submit reviews with structured feedback
- Audit trail of all submissions and reviews

🔒 **Document Security**
- PDF watermarking with institutional branding (institution name and logo)
- File upload and storage
- Download tracking and file management

## Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: MySQL
- **Authentication**: Argon2 password hashing
- **Email**: SMTP integration for OTP delivery
- **File Processing**: PyPDF2, ReportLab for PDF manipulation

### Frontend
- **HTML5** for semantic markup
- **CSS3** for responsive design with particle effects
- **JavaScript** for interactive features and animation

### Security & Infrastructure
- Environment variable configuration via `.env`
- CSRF protection with session signing
- Configurable session lifetimes
- Live reload support for development


## Project Structure

```
UniScholarWorks/
├── static/               # Client-side assets
│   ├── images/           # Logo & other images
│   ├── scripts/          # JavaScript modules
│   └── styles/           # CSS stylesheets
├── templates/            # HTML templates
├── venv/                 # Virtual environment
├── .gitignore            # Git ignored files
├── app.py                # Flask application & route handlers
├── database_queries.py   # Database operations & queries
├── my_classes.py         # Data models (User, Report classes)
└── my_utilities.py       # Utility functions (PDF watermarking, email, AI summary)
```
