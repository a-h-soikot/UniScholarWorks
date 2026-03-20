# UniScholarWorks – An Academic Thesis, Research Repository

UniScholarWorks is a full-stack web application built with the goal of streamlining the submission, tracking, review, and reading process of academic reports within a university environment. The platform supports dual-user roles (students and teachers) with role-based features, secure authentication, and document management.


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

## <p align="left" margin-bottom:0px>  Tech Stack <a href="https://www.python.org" target="_blank"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="28" height="28"/></a> <a href="https://www.mysql.com/" target="_blank"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original-wordmark.svg" width="28" height="28"/></a> <a href="https://developer.mozilla.org/en-US/docs/Web/HTML" target="_blank"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" width="28" height="28"/></a> <a href="https://developer.mozilla.org/en-US/docs/Web/CSS" target="_blank"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" width="28" height="28"/></a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" width="28" height="28"/></a> </p>

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
