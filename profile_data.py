"""
Portfolio Profile Data
Extracted strictly from P. Benarji Rathnam's verified resume.
No invented statistics, certifications, or work experience.
"""

PROFILE = {
    "name": "P. Benarji Rathnam",
    "short_name": "Benarji",
    "headline": "Software Developer | Full Stack Developer | AWS & DevOps",
    "location": "Hyderabad, Telangana, India",
    "phone": "+91 6303066179",
    "email": "benarjip69@gmail.com",
    "linkedin": "https://www.linkedin.com/in/benarji-p-126a52305",
    "github": "https://github.com/benarjip",
    "summary": (
        "Computer Engineering undergraduate and aspiring Full Stack & AI/ML Developer "
        "with hands-on experience building full-stack web applications and blockchain-based "
        "systems. Recognized as 'Best Performer' during AI/ML internship. Skilled in Python, "
        "JavaScript, React.js, Django, Node.js, and cloud/DevOps fundamentals."
    ),
    "availability": "Available for Full-Time & Internship Opportunities",
    "strengths": [
        "Positive Attitude",
        "Team Collaboration & Social Interaction",
        "Hardworking & Detail-Oriented",
        "Creative Problem Solving",
        "Consistent & Fast Learner",
    ],
    "languages_spoken": ["English", "Hindi", "Telugu"],
    "hobbies": ["Volleyball", "Leather Ball Cricket", "Reading", "Exploring Tech", "Travelling"],
}

EXPERIENCE = [
    {
        "role": "AI & Machine Learning Intern",
        "company": "Elevate Labs",
        "period": "June 2025 – July 2025",
        "location": "Remote",
        "badge": "Best Performer Awarded",
        "highlights": [
            "Completed an intensive 5-week Artificial Intelligence and Machine Learning internship, applying core ML concepts and analytical techniques to real-world tasks under mentorship.",
            "Recognized as 'Best Performer' for exceptional skill, consistency, and dedication among the intern cohort.",
            "Strengthened practical expertise in data analysis, model evaluation, systematic problem-solving, and cross-functional technical communication.",
        ],
        "technologies": ["Python", "Machine Learning", "Data Analysis", "Jupyter Notebook"],
    }
]

PROJECTS = [
    {
        "id": "e-voting-blockchain",
        "title": "E-Voting System Using Blockchain",
        "period": "2025",
        "category": "Full Stack / Blockchain",
        "problem_statement": (
            "Traditional electronic voting systems suffer from centralized points of failure, "
            "vulnerability to database tampering, lack of voter auditability, and potential "
            "double-voting risks that weaken democratic trust."
        ),
        "solution": (
            "Engineered a secure, decentralized e-voting platform using Ethereum smart contracts "
            "to guarantee cryptographic immutability, mathematically eliminate double voting, and "
            "deliver transparent, verifiable election results."
        ),
        "key_features": [
            "Architected full-stack application using Django for backend REST services and React.js for interactive frontend.",
            "Designed Solidity smart contracts compiled and deployed on Ganache to enforce strict one-vote-per-voter logic.",
            "Integrated MetaMask wallet authentication for cryptographic transaction signing and ballot authorization.",
            "Implemented Aadhaar-based voter verification pipeline with email OTP verification for identity validation.",
            "Built administrative dashboard with SQLite managing voter records, real-time vote counting, and instantaneous tally generation.",
        ],
        "technologies": [
            "Python",
            "Django",
            "React.js",
            "Solidity",
            "Ethereum",
            "Ganache",
            "MetaMask",
            "SQLite",
        ],
        "github_url": "https://github.com/benarjip/evoting-blockchain",
        "live_url": None,
        "status_badge": "Completed",
        "mockup_type": "blockchain-voting",
    },
    {
        "id": "grocery-tracking-app",
        "title": "Grocery Tracking Application",
        "period": "Jan – Oct 2025",
        "category": "Full Stack / MERN",
        "problem_statement": (
            "Households routinely waste significant food and overspend due to poor visibility into "
            "pantry inventory, missed expiration dates, and lack of organized expense tracking."
        ),
        "solution": (
            "Developed an intuitive full-stack web application enabling users to catalog grocery "
            "purchases, monitor daily expenses, track perishable item shelf life, and systematically "
            "reduce household food wastage."
        ),
        "key_features": [
            "Engineered robust RESTful backend APIs with Node.js and Express.js, integrating MongoDB for resilient data persistence.",
            "Implemented full CRUD functionality for instant item addition, shelf-life updates, and real-time inventory adjustments.",
            "Designed a responsive React-based interface featuring dashboards for purchase history, monthly spend analytics, and expiry alerts.",
            "Implemented category-based filtering, budget tracking, and smart notifications for low-stock and expiring items.",
            "Architected scalability blueprints including barcode/QR code scanning, multi-user household synchronization, and AI-driven predictive grocery suggestions.",
        ],
        "technologies": [
            "React.js",
            "Node.js",
            "Express.js",
            "MongoDB",
            "REST APIs",
            "JavaScript (ES6+)",
        ],
        "github_url": "https://github.com/benarjip/grocery-tracking-app",
        "live_url": None,
        "status_badge": "Completed",
        "mockup_type": "grocery-inventory",
    },
]

EDUCATION = [
    {
        "degree": "B.Tech in Computer Engineering",
        "institution": "Matrusri Engineering College",
        "location": "Hyderabad, Telangana, India",
        "period": "2022 – Present",
        "grade": "CGPA: 7.0",
        "status": "Final Year Undergraduate",
        "details": "Core coursework in Data Structures, Object-Oriented Programming, Database Management Systems, Software Engineering, Operating Systems, and Computer Networks.",
    },
    {
        "degree": "Intermediate (MPC)",
        "institution": "Global Junior College",
        "location": "Telangana, India",
        "period": "2020 – 2022",
        "grade": "Score: 5.81",
        "status": "Completed",
        "details": "Focus on Mathematics, Physics, and Chemistry.",
    },
    {
        "degree": "SSC (Secondary School Certificate)",
        "institution": "TSWREIS Govt. School, Parigi",
        "location": "Telangana, India",
        "period": "2019 – 2020",
        "grade": "GPA: 9.5 / 10.0",
        "status": "Completed",
        "details": "Top-tier academic performance with 9.5 GPA in Telangana state board curriculum.",
    },
]

SKILL_CATEGORIES = [
    {
        "name": "Programming Languages",
        "icon": "code",
        "description": "Core languages for systems, algorithms, and application development",
        "skills": ["Python", "Java", "C", "JavaScript (ES6+)", "SQL", "Solidity"],
    },
    {
        "name": "Frontend Development",
        "icon": "layout",
        "description": "Building responsive, modern, user-centric web applications",
        "skills": ["HTML5", "CSS3", "JavaScript", "React.js", "Responsive UI", "DOM Manipulation"],
    },
    {
        "name": "Backend Development",
        "icon": "server",
        "description": "Server-side architectures, RESTful APIs, and business logic",
        "skills": ["Python", "Django", "Node.js", "Express.js", "REST APIs", "CRUD Architectures"],
    },
    {
        "name": "Databases",
        "icon": "database",
        "description": "Relational and document storage solutions for scalable applications",
        "skills": ["MongoDB", "SQLite", "MySQL", "Data Modeling"],
    },
    {
        "name": "AWS & Cloud Computing",
        "icon": "cloud",
        "description": "Serverless architectures, cloud storage, edge distribution, and security",
        "skills": [
            "Amazon Route 53",
            "Amazon CloudFront",
            "Amazon S3",
            "Amazon API Gateway",
            "AWS Lambda",
            "Amazon DynamoDB",
            "Amazon SES",
            "AWS IAM",
            "Amazon CloudWatch",
            "AWS Certificate Manager (ACM)",
        ],
    },
    {
        "name": "DevOps & Tooling",
        "icon": "git-branch",
        "description": "Version control, developer tooling, and modern deployment practices",
        "skills": ["Git", "GitHub", "Linux / Shell", "VS Code", "Jupyter Notebook", "Postman", "CI/CD Fundamentals"],
    },
    {
        "name": "Blockchain & Web3",
        "icon": "link",
        "description": "Decentralized applications, smart contracts, and Web3 integration",
        "skills": ["Solidity", "Ethereum", "Ganache", "MetaMask", "Smart Contracts", "Web3 Principles"],
    },
    {
        "name": "AI & Machine Learning",
        "icon": "cpu",
        "description": "Applied ML concepts, exploratory data analysis, and predictive workflows",
        "skills": [
            "Machine Learning Fundamentals",
            "Data Analytics",
            "Model Evaluation",
            "Feature Engineering",
            "Jupyter Notebook",
        ],
    },
]

CERTIFICATIONS = [
    {
        "title": "Artificial Intelligence and Machine Learning Internship",
        "issuer": "Elevate Labs",
        "year": "2025",
        "badge": "Best Performer",
        "description": "5-week intensive hands-on internship in applied AI & ML, earning top cohort honors for analytical excellence and dedication.",
    },
    {
        "title": "Data Analytics Job Simulation",
        "issuer": "Deloitte Australia (Forage)",
        "year": "2024",
        "badge": "Verified Simulation",
        "description": "Practical simulation covering business data analysis, forensic analytics, and visualization to provide strategic decision insights.",
    },
]

ACHIEVEMENTS = [
    {
        "title": "Best Performer Recognition",
        "organization": "Elevate Labs",
        "category": "Academic & Professional",
        "description": "Awarded Best Performer for exceptional analytical skill, consistency, and project delivery during AI/ML internship.",
    },
    {
        "title": "State-Level Merit Certificate in Volleyball",
        "organization": "School Games Federation (SGF)",
        "category": "Athletics & Sportsmanship",
        "description": "Competed and earned state-level merit honors in volleyball, cultivating teamwork, discipline, and endurance under pressure.",
    },
    {
        "title": "Local Tournament Winner",
        "organization": "Leather Ball Cricket",
        "category": "Athletics & Leadership",
        "description": "Championship winner in competitive leather ball cricket tournament.",
    },
]

AWS_ARCHITECTURE = {
    "status": "Planned Production Architecture",
    "overview": (
        "This portfolio is engineered with an AWS-first architectural blueprint. "
        "It decouples ultra-fast, globally-distributed static delivery from an event-driven, "
        "pay-per-request serverless backend for contact processing, ensuring maximum speed, "
        "rock-solid security, and near-zero operating cost."
    ),
    "hosting_pipeline": [
        {
            "step": "1",
            "service": "Amazon Route 53",
            "role": "Global DNS Management",
            "description": "Highly available and scalable cloud Domain Name System (DNS) routing user requests with sub-millisecond response latency and automatic health checking.",
        },
        {
            "step": "2",
            "service": "Amazon CloudFront",
            "role": "Global Content Delivery Network",
            "description": "Global edge caching layer delivering static assets with ultra-low latency, enforcing TLS 1.3 termination, and shielding backend origins.",
        },
        {
            "step": "3",
            "service": "Amazon S3",
            "role": "Origin Static Storage",
            "description": "Serverless object storage hosting the optimized portfolio frontend assets with 99.999999999% (11 9's) durability, restricted via Origin Access Control (OAC).",
        },
        {
            "step": "4",
            "service": "Portfolio Client",
            "role": "Fast Browser Rendering",
            "description": "Delivers an instantaneous, smooth, interactive dark-themed portfolio directly to the client's browser.",
        },
    ],
    "contact_pipeline": [
        {
            "step": "1",
            "service": "Client Contact Form",
            "role": "CSRF & Client Validation",
            "description": "Submits sanitized messages via asynchronous HTTPS requests with client-side rate limit awareness.",
        },
        {
            "step": "2",
            "service": "Amazon API Gateway",
            "role": "Managed REST Endpoint",
            "description": "Acts as the secure front door, enforcing throttle limits, request payload validation, and CORS policies before invoking compute.",
        },
        {
            "step": "3",
            "service": "AWS Lambda (Python 3.13)",
            "role": "Serverless Compute Handler",
            "description": "Executes input sanitization, spam scoring, and dispatches parallel writes to DynamoDB and emails through SES without managing servers.",
        },
        {
            "step": "4a",
            "service": "Amazon DynamoDB",
            "role": "Auditable NoSQL Store",
            "description": "Stores timestamped contact submissions in a flexible, on-demand table with encryption-at-rest (KMS) for auditable history.",
        },
        {
            "step": "4b",
            "service": "Amazon SES",
            "role": "High-Deliverability Email Service",
            "description": "Dispatches formatted notification emails with DKIM/SPF verification directly to Benarji's inbox without third-party email exposure.",
        },
    ],
    "supporting_services": [
        {
            "service": "AWS IAM",
            "title": "Identity & Access Management",
            "badge": "Least Privilege",
            "description": "Strict role-based policies granting Lambda execution permissions only to specific DynamoDB PutItem and SES SendEmail actions.",
        },
        {
            "service": "Amazon CloudWatch",
            "title": "Observability & Metrics",
            "badge": "Logging & Alarms",
            "description": "Centralized logs for API Gateway access and Lambda executions, with threshold alarms alerting on unexpected error rates.",
        },
        {
            "service": "AWS Certificate Manager (ACM)",
            "title": "Automated SSL/TLS",
            "badge": "Free Auto-Renewal",
            "description": "Provisions and automatically renews public SSL/TLS certificates for custom domain HTTPS security across CloudFront and Route 53.",
        },
        {
            "service": "AWS WAF",
            "title": "Web Application Firewall",
            "badge": "Optional Security Layer",
            "description": "Layer 7 security inspection blocking SQL injection attempts, malicious bots, and rate-abusing IP ranges at the CloudFront edge.",
        },
    ],
}
