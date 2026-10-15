import json
import pytest
from app import create_app


@pytest.fixture
def app():
    """Create and configure a clean testing app instance."""
    app_instance = create_app("testing")
    app_instance.config.update(
        {
            "TESTING": True,
            "RATE_LIMIT_REQUESTS": 4,
            "RATE_LIMIT_WINDOW_SECONDS": 60,
        }
    )
    return app_instance


@pytest.fixture
def client(app):
    """Test client for HTTP requests."""
    return app.test_client()


def get_csrf_token(client):
    """Helper to fetch a valid CSRF token from the session/page."""
    response = client.get("/")
    assert response.status_code == 200
    with client.session_transaction() as sess:
        return sess.get("csrf_token")


def test_home_page_renders_centered_hero(client):
    """Verify that the home page renders 200 with the single-column centered hero."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    # Required Hero Elements
    assert "P. Benarji Rathnam" in html
    assert ("Software Developer | Full Stack Developer | AWS &amp; DevOps" in html or 
            "Software Developer | Full Stack Developer | AWS & DevOps" in html)
    assert "Available for Full-Time" in html
    assert "hero-container" in html
    assert "hero-actions" in html
    assert "View Projects" in html
    assert "Download Resume" in html

    # Required Sections
    assert 'id="about"' in html
    assert 'id="skills"' in html
    assert 'id="projects"' in html
    assert 'id="experience"' in html
    assert 'id="education"' in html
    assert 'id="aws-architecture"' in html
    assert 'id="contact"' in html

    # Resume Verified Content
    assert "E-Voting System Using Blockchain" in html
    assert "Grocery Tracking Application" in html
    assert "Elevate Labs" in html
    assert "Best Performer" in html
    assert "Matrusri Engineering College" in html


def test_about_page(client):
    """Verify the dedicated about page renders successfully."""
    response = client.get("/about")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "P. Benarji Rathnam" in html
    assert "Matrusri Engineering College" in html
    assert "Elevate Labs" in html


def test_projects_page(client):
    """Verify the dedicated projects page renders projects from resume."""
    response = client.get("/projects")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "E-Voting System Using Blockchain" in html
    assert "Grocery Tracking Application" in html
    assert "Solidity" in html
    assert "MongoDB" in html


def test_contact_page_get(client):
    """Verify contact page GET returns form with CSRF token."""
    response = client.get("/contact")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "name" in html
    assert "email" in html
    assert "message" in html
    assert "csrf_token" in html


def test_health_check(client):
    """Verify health check endpoint returns 200 and healthy JSON."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


def test_resume_download(client):
    """Verify the resume endpoint serves the PDF file."""
    # Test inline view
    response = client.get("/resume")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"

    # Test download attachment
    response_download = client.get("/resume?download=1")
    assert response_download.status_code == 200
    assert response_download.headers["Content-Type"] == "application/pdf"
    assert "attachment" in response_download.headers.get("Content-Disposition", "")


def test_security_headers(client):
    """Verify essential security headers are applied to responses."""
    response = client.get("/")
    headers = response.headers
    assert headers.get("X-Content-Type-Options") == "nosniff"
    assert headers.get("X-Frame-Options") == "SAMEORIGIN"
    assert headers.get("X-XSS-Protection") == "1; mode=block"
    assert "strict-origin-when-cross-origin" in headers.get("Referrer-Policy", "")
    assert "Content-Security-Policy" in headers


def test_contact_form_valid_submission(client):
    """Verify submitting contact form with valid CSRF succeeds in local dev mode."""
    csrf_token = get_csrf_token(client)
    payload = {
        "csrf_token": csrf_token,
        "name": "Recruiter Alice",
        "email": "alice@company.com",
        "subject": "Interview Invitation",
        "message": "We reviewed your portfolio and would love to schedule a technical discussion.",
        "website": "",
    }
    response = client.post(
        "/contact",
        data=json.dumps(payload),
        content_type="application/json",
        headers={"X-CSRFToken": csrf_token},
    )
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert data["success"] is True


def test_contact_form_missing_csrf(client):
    """Verify submitting contact form without CSRF is rejected with 400."""
    payload = {
        "name": "Attacker",
        "email": "attacker@evil.com",
        "message": "Attempting cross site request forgery.",
    }
    response = client.post(
        "/contact",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert data["success"] is False
    assert "CSRF" in data["message"] or "validation" in data["message"].lower()


def test_contact_form_invalid_email(client):
    """Verify invalid email address triggers validation error."""
    csrf_token = get_csrf_token(client)
    payload = {
        "csrf_token": csrf_token,
        "name": "Jane Doe",
        "email": "invalid-email-no-domain",
        "message": "Hello Benarji, this is a test message.",
        "website": "",
    }
    response = client.post(
        "/contact",
        data=json.dumps(payload),
        content_type="application/json",
        headers={"X-CSRFToken": csrf_token},
    )
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert data["success"] is False
    assert "valid email" in data["message"].lower()


def test_contact_form_short_message(client):
    """Verify message shorter than 10 characters is rejected."""
    csrf_token = get_csrf_token(client)
    payload = {
        "csrf_token": csrf_token,
        "name": "Jane Doe",
        "email": "jane@example.com",
        "message": "Hi",  # Too short
        "website": "",
    }
    response = client.post(
        "/contact",
        data=json.dumps(payload),
        content_type="application/json",
        headers={"X-CSRFToken": csrf_token},
    )
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert data["success"] is False
    assert "10" in data["message"]


def test_contact_honeypot_blocking(client):
    """Verify bot filling out honeypot field is silently trapped."""
    csrf_token = get_csrf_token(client)
    payload = {
        "csrf_token": csrf_token,
        "name": "Spam Bot",
        "email": "spambot@spam.com",
        "message": "Buy crypto now and get rich quick!",
        "website": "http://spamsite.com",  # Honeypot filled
    }
    response = client.post(
        "/contact",
        data=json.dumps(payload),
        content_type="application/json",
        headers={"X-CSRFToken": csrf_token},
    )
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert data["success"] is True


def test_contact_rate_limiting(client):
    """Verify submitting too many messages in a short window returns 429."""
    csrf_token = get_csrf_token(client)
    payload = {
        "csrf_token": csrf_token,
        "name": "Rapid Submitter",
        "email": "rapid@example.com",
        "message": "Testing the in-memory rate limiter limit.",
        "website": "",
    }

    # Our test limit is set to 4 requests in fixture
    for _ in range(4):
        res = client.post(
            "/contact",
            data=json.dumps(payload),
            content_type="application/json",
            headers={"X-CSRFToken": csrf_token},
        )
        assert res.status_code == 200

    # 5th request must be rate-limited (HTTP 429)
    res_rate_limited = client.post(
        "/contact",
        data=json.dumps(payload),
        content_type="application/json",
        headers={"X-CSRFToken": csrf_token},
    )
    assert res_rate_limited.status_code == 429
    data = json.loads(res_rate_limited.get_data(as_text=True))
    assert "Too many requests" in data["message"]


def test_404_handler(client):
    """Verify unknown URL renders custom 404 page."""
    response = client.get("/non-existent-page-xyz")
    assert response.status_code == 404
    html = response.get_data(as_text=True)
    assert "404" in html
    assert "Page Not Found" in html
