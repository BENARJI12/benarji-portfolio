import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the application
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file if present
load_dotenv(BASE_DIR / ".env")


class Config:
    """Base application configuration."""

    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "fallback-secret-key-dev-purposes-only-32bytes"
    )

    DEBUG = False
    TESTING = False

    # Security & Session Settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False  # Enabled in ProductionConfig
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB max payload to protect server

    # Profile & Recipient Details
    PORTFOLIO_OWNER_NAME = os.environ.get(
        "PORTFOLIO_OWNER_NAME", "P. Benarji Rathnam"
    )
    PORTFOLIO_OWNER_HEADLINE = "Software Developer | Full Stack Developer | AWS & DevOps"
    PORTFOLIO_OWNER_LOCATION = "Hyderabad, India"
    CONTACT_RECIPIENT_EMAIL = os.environ.get(
        "CONTACT_RECIPIENT_EMAIL", "benarjip69@gmail.com"
    )
    PORTFOLIO_PHONE = "+91 6303066179"
    PORTFOLIO_LINKEDIN = "https://www.linkedin.com/in/benarji-p-126a52305"
    PORTFOLIO_GITHUB = "https://github.com/benarjip"

    # Email Service (SMTP)
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "").strip()
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "").strip()
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "").strip()
    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER", f"P. Benarji Rathnam Portfolio <{CONTACT_RECIPIENT_EMAIL}>"
    )

    # In-Memory Rate Limiting
    RATE_LIMIT_REQUESTS = int(os.environ.get("RATE_LIMIT_REQUESTS", 5))
    RATE_LIMIT_WINDOW_SECONDS = int(os.environ.get("RATE_LIMIT_WINDOW_SECONDS", 600))

    # AWS Planned Infrastructure Config
    AWS_REGION = os.environ.get("AWS_REGION", "ap-south-1")
    DYNAMODB_TABLE_NAME = os.environ.get(
        "DYNAMODB_TABLE_NAME", "PortfolioContactSubmissions"
    )
    SES_SENDER_EMAIL = os.environ.get("SES_SENDER_EMAIL", "benarjip69@gmail.com")


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production environment configuration with strict security."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = True
    SECRET_KEY = "test-secret-key-for-automated-suites"
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW_SECONDS = 60


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
