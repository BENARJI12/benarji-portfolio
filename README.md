# P. Benarji Rathnam — Professional Developer Portfolio

A modern, fast, secure, and production-ready personal portfolio website built with **Python**, **Flask**, **HTML5**, **CSS3**, **Vanilla JavaScript**, and **Jinja2 templates**.

All professional information, projects, skills, education, certifications, and achievements are strictly sourced from P. Benarji Rathnam's verified resume.

---

## 🌟 Key Highlights & Design Decisions

- **Single-Column Centered Hero Section (Fixes Prior UI Issue)**:
  - The hero is centered horizontally and vertically beneath the sticky navbar across all screen sizes (desktop, laptop, tablet, and mobile).
  - Eliminates the previous two-column layout that left an empty left margin.
  - Built with pure CSS Flexbox (`display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin: 0 auto;`).
- **Curated Dark Aesthetic**:
  - Charcoal / near-black foundation (`#0b0e14`, `#121620`, `#161c28`) with high-contrast text (`#f8fafc`).
  - Sleek purple-to-pink gradient accents (`linear-gradient(135deg, #a855f7 0%, #ec4899 100%)`) with subtle cyan/blue highlights (`#38bdf8`).
  - Glassmorphic navigation bar with backdrop blur and active section indicator.
- **Categorized Technical Skills**:
  - Distinct cards for Programming, Frontend, Backend, Databases, AWS & Cloud Computing, DevOps, Blockchain, and AI/ML.
  - No fake percentage bars; real-world competencies only.
- **Featured Projects**:
  - **E-Voting System Using Blockchain** (Python, Django, React.js, Solidity, Ethereum, Ganache, MetaMask, SQLite).
  - **Grocery Tracking Application** (React.js, Node.js, Express.js, MongoDB, REST APIs).
  - Complete with problem statement, engineering solution, key features, and source code links.
- **Work Experience & Verified Honors**:
  - Elevate Labs (AI & Machine Learning Intern) with verified **"Best Performer"** award.
  - State-Level Merit Certificate in Volleyball (School Games Federation).
  - Local Tournament Winner in Leather Ball Cricket.
- **"Built for AWS" Architecture Showcase**:
  - Interactive HTML/CSS diagram illustrating the planned production architecture.
  - Detailed explanation of Route 53, CloudFront, S3, API Gateway, AWS Lambda, DynamoDB, SES, IAM, CloudWatch, and ACM.
- **Production-Grade Python/Flask Backend**:
  - Automated CSRF protection with cryptographic tokens.
  - Server-side email and length validation.
  - Client-side and server-side rate limiting (prevents spam and denial of service).
  - Hidden anti-abuse honeypot field.
  - Safe local development mode (logs submissions safely without exposing credentials) and SMTP support for Amazon SES or Gmail.
  - PDF resume download endpoint (`/resume?download=1`) serving the real verified resume.
  - Comprehensive health check endpoint (`/health`).
  - Custom branded 404 and 500 error pages.

---

## 📁 Project Directory Structure

```text
Benarji PF/
├── app.py                     # Flask application factory, routes, CSRF, security headers, rate limiting
├── config.py                  # Environment-driven configuration (Dev, Prod, Test)
├── profile_data.py            # Exact structured data extracted from verified resume
├── requirements.txt           # Python dependencies
├── .env.example               # Template for environment variables and secrets
├── .env                       # Local development environment configuration
├── .gitignore                 # Excludes caches, secrets, logs, and venvs
├── README.md                  # Comprehensive documentation and AWS deployment guide
├── templates/                 # Jinja2 templates
│   ├── base.html              # Base layout with navbar, footer, SEO tags, flash alerts
│   ├── index.html             # Master single-page portfolio with centered hero
│   ├── about.html             # Dedicated About page
│   ├── projects.html          # Dedicated Projects page
│   ├── contact.html           # Dedicated Contact page
│   ├── 404.html               # Custom 404 Not Found error page
│   └── 500.html               # Custom 500 Internal Server Error page
├── static/
│   ├── css/
│   │   └── style.css          # Design system, centered hero, responsive styles, AWS diagrams
│   ├── js/
│   │   └── script.js          # Mobile nav, smooth scroll, active observer, AJAX contact submission
│   ├── files/
│   │   └── resume.pdf         # Verified PDF resume file for downloads
│   └── images/                # Project assets and graphics
└── tests/
    └── test_app.py            # 14 automated pytest test cases
```

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.13)
- pip package manager

### 2. Clone / Open Directory
```bash
cd "c:\Users\benar\Downloads\Benarji PF"
```

### 3. Create a Virtual Environment (Recommended)
```bash
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Default values in `.env` are pre-configured for safe local testing out of the box.

### 6. Run the Application
```bash
python app.py
```
Open your browser at `http://127.0.0.1:5000`.

---

## 🧪 Running Automated Tests

Run the full pytest suite with verbose output:
```bash
python -m pytest tests/test_app.py -v
```

The test suite validates:
1. Centered hero rendering and required profile information
2. Dedicated routes (`/about`, `/projects`, `/contact`)
3. Health check JSON endpoint (`/health`)
4. Resume download and inline view (`/resume`)
5. Security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`, etc.)
6. Contact form validation (valid submission, missing CSRF rejection, malformed email detection, short message detection)
7. Anti-abuse honeypot silent trap
8. In-memory IP rate limiting (HTTP 429)
9. Custom 404 handler

---

## ✉️ Contact Form Configuration

The contact form supports two execution modes:

### 1. Safe Local Development Mode (Default)
When `MAIL_SERVER` or `MAIL_USERNAME` is left blank in `.env`, submissions are validated, CSRF-checked, rate-limited, and logged safely to the server console:
```text
[LOCAL DEV CONTACT SUBMISSION]
From: Recruiter Name <recruiter@company.com>
Subject: Software Developer Role
IP: 127.0.0.1
Message: We would like to schedule an interview with you.
```
The client receives a clear confirmation message informing them that the submission was recorded in development mode. No false delivery claims are made.

### 2. Production SMTP Dispatch (Amazon SES or Gmail)
To enable real email dispatch, set the following in `.env`:
```env
MAIL_SERVER=email-smtp.ap-south-1.amazonaws.com # or smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-ses-smtp-username
MAIL_PASSWORD=your-ses-smtp-password
MAIL_DEFAULT_SENDER="P. Benarji Rathnam Portfolio <benarjip69@gmail.com>"
CONTACT_RECIPIENT_EMAIL=benarjip69@gmail.com
```

---

## ☁️ "Built for AWS" Architecture & Deployment Strategy

The application is engineered with an AWS-first architectural blueprint. Two primary deployment patterns are supported:

### Pattern A: Decoupled Jamstack (Static Frontend + Serverless Backend)
Ideal for maximum performance, 100% serverless scale, and minimal operating cost:
1. **Frontend Hosting**:
   - `templates/` and `static/` are generated/packaged into HTML, CSS, and JS assets.
   - Hosted on an **Amazon S3** bucket with private access restricted by **Origin Access Control (OAC)**.
   - Distributed globally through **Amazon CloudFront** edge points of presence with TLS 1.3 termination.
   - Managed DNS routing via **Amazon Route 53** with SSL/TLS certificate from **AWS Certificate Manager (ACM)**.
2. **Contact Processing Backend**:
   - The `/contact` endpoint routes to **Amazon API Gateway** (REST API) with throttling and CORS enabled.
   - Invokes an **AWS Lambda (Python 3.13)** function that performs input sanitization and spam detection.
   - Saves submission audit trails in **Amazon DynamoDB** with encryption-at-rest.
   - Sends notification emails via **Amazon SES** (Simple Email Service).

```text
[User]
   │
   ▼
[Route 53] ──▶ [CloudFront CDN] ──▶ [S3 Bucket: Static Assets]
                      │
   [Contact Form Submission]
                      ▼
             [API Gateway]
                      │
                      ▼
             [AWS Lambda (Python)]
                ├──▶ [Amazon DynamoDB] (Encrypted Store)
                └──▶ [Amazon SES] (Verified Email Dispatch)
```

### Pattern B: Full Flask Container Deployment (AWS App Runner / Elastic Beanstalk)
To run the full dynamic Flask application directly in the cloud:
1. **AWS App Runner** (Recommended for Flask):
   - Fully managed container service with automatic load balancing, TLS encryption, and auto-scaling.
   - Point App Runner to the repository or ECR container image; specify build command `pip install -r requirements.txt` and start command `gunicorn -w 4 -b 0.0.0.0:8080 app:app`.
2. **Supporting AWS Services**:
   - **AWS IAM**: Role with least-privilege permissions (`ses:SendEmail`, `dynamodb:PutItem`).
   - **Amazon CloudWatch**: Detailed request logging, error metrics, and alarm triggers.
   - **AWS WAF**: Edge firewall rules protecting against OWASP Top 10 vulnerabilities.

---

## 🛡️ Security Implementation

- **CSRF Protection**: Cryptographic tokens generated per session, validated on all state-changing POST requests.
- **Input Sanitization**: Strict server-side checks on all form fields preventing script injection or payload inflation.
- **Rate Limiting**: Rolling window limiter preventing automated spam floods.
- **Honeypot Trap**: Invisible decoy input fields that trap automated spam bots without burdening human visitors.
- **Security Headers**:
  - `Content-Security-Policy`: Restricts unauthorized scripts, objects, and external connections.
  - `X-Frame-Options: SAMEORIGIN`: Defends against clickjacking.
  - `X-Content-Type-Options: nosniff`: Prevents MIME-type sniffing.
  - `Referrer-Policy: strict-origin-when-cross-origin`: Guards sensitive referrer data.
  - `Permissions-Policy`: Restricts camera, microphone, and geolocation.
- **Zero Exposed Credentials**: All secrets reside strictly in `.env`, excluded via `.gitignore`.

---

## 👤 Author & Contact

**P. Benarji Rathnam**  
Software Developer | Full Stack Developer | AWS & DevOps  
- **Location**: Hyderabad, Telangana, India  
- **Email**: [benarjip69@gmail.com](mailto:benarjip69@gmail.com)  
- **Phone**: +91 6303066179  
- **LinkedIn**: [linkedin.com/in/benarji-p-126a52305](https://www.linkedin.com/in/benarji-p-126a52305)  
- **GitHub**: [github.com/benarjip](https://github.com/benarjip)
