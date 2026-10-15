import os
import re
import secrets
import smtplib
import time
import logging
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash,
    send_file,
    session,
    abort,
)

from config import config_by_name, BASE_DIR
from profile_data import (
    PROFILE,
    EXPERIENCE,
    PROJECTS,
    EDUCATION,
    SKILL_CATEGORIES,
    CERTIFICATIONS,
    ACHIEVEMENTS,
    AWS_ARCHITECTURE,
)

# Setup structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("portfolio")


def create_app(config_name=None):
    """Application factory for Flask portfolio app."""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    config_class = config_by_name.get(config_name, config_by_name["default"])
    app.config.from_object(config_class)

    # In-memory storage for rate limiting: {client_ip: [timestamp1, timestamp2, ...]}
    ip_request_history = {}

    def get_client_ip():
        """Retrieve client IP address, respecting reverse proxies securely."""
        if request.headers.get("X-Forwarded-For"):
            # Return first IP from proxy chain
            return request.headers.get("X-Forwarded-For").split(",")[0].strip()
        return request.remote_addr or "127.0.0.1"

    def check_rate_limit(ip):
        """Check if client IP exceeds allowed rate limit."""
        now = time.time()
        window = app.config.get("RATE_LIMIT_WINDOW_SECONDS", 600)
        max_requests = app.config.get("RATE_LIMIT_REQUESTS", 5)

        timestamps = ip_request_history.get(ip, [])
        # Filter timestamps within the active time window
        active_timestamps = [t for t in timestamps if now - t < window]

        if len(active_timestamps) >= max_requests:
            ip_request_history[ip] = active_timestamps
            return False, int(window - (now - active_timestamps[0]))

        active_timestamps.append(now)
        ip_request_history[ip] = active_timestamps
        return True, 0

    def generate_csrf_token():
        """Generate and store CSRF token in session if not already set."""
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_hex(32)
        return session["csrf_token"]

    def validate_csrf_token():
        """Validate CSRF token from form or header against session."""
        session_token = session.get("csrf_token")
        if not session_token:
            return False

        # Check form data, JSON payload, or header
        submitted_token = (
            request.form.get("csrf_token")
            or (request.is_json and request.get_json(silent=True) or {}).get("csrf_token")
            or request.headers.get("X-CSRFToken")
        )

        if not submitted_token:
            return False

        return secrets.compare_digest(session_token, submitted_token)

    # Context processors: make CSRF token, current year, and profile available in all templates
    @app.context_processor
    def inject_globals():
        return {
            "csrf_token": generate_csrf_token,
            "current_year": datetime.now().year,
            "profile": PROFILE,
        }

    # Security headers on every response
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=()"
        )

        # Content Security Policy (allows Google Fonts, inline styles for themes, and standard media)
        csp = (
            "default-src 'self'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com data:; "
            "img-src 'self' data: https:; "
            "script-src 'self' 'unsafe-inline'; "
            "connect-src 'self'; "
            "frame-ancestors 'self';"
        )
        response.headers["Content-Security-Policy"] = csp

        if app.config.get("SESSION_COOKIE_SECURE"):
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        return response

    # -------------------------------------------------------------
    # Routes
    # -------------------------------------------------------------

    @app.route("/")
    def index():
        """Home page with single-column centered hero and all sections."""
        return render_template(
            "index.html",
            profile=PROFILE,
            experience=EXPERIENCE,
            projects=PROJECTS,
            education=EDUCATION,
            skill_categories=SKILL_CATEGORIES,
            certifications=CERTIFICATIONS,
            achievements=ACHIEVEMENTS,
            aws_architecture=AWS_ARCHITECTURE,
            active_page="home",
        )

    @app.route("/about")
    def about():
        """Dedicated About page highlighting background, skills, and education."""
        return render_template(
            "about.html",
            profile=PROFILE,
            experience=EXPERIENCE,
            education=EDUCATION,
            skill_categories=SKILL_CATEGORIES,
            certifications=CERTIFICATIONS,
            achievements=ACHIEVEMENTS,
            active_page="about",
        )

    @app.route("/projects")
    def projects():
        """Dedicated Projects page showcasing full project specs and architecture."""
        return render_template(
            "projects.html",
            profile=PROFILE,
            projects=PROJECTS,
            active_page="projects",
        )

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        """Contact page & secure submission handler."""
        if request.method == "GET":
            return render_template(
                "contact.html",
                profile=PROFILE,
                active_page="contact",
            )

        # POST submission handler
        client_ip = get_client_ip()

        # 1. Rate limiting check
        allowed, retry_after = check_rate_limit(client_ip)
        if not allowed:
            error_msg = (
                f"Too many requests. Please wait {retry_after} seconds before submitting again."
            )
            if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "message": error_msg}), 429
            flash(error_msg, "error")
            return redirect(url_for("contact") + "#contact-form")

        # 2. CSRF Token Validation
        if not validate_csrf_token():
            error_msg = "Security validation failed (invalid or expired CSRF token). Please refresh and try again."
            logger.warning("CSRF validation failure from IP %s", client_ip)
            if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "message": error_msg}), 400
            flash(error_msg, "error")
            return redirect(url_for("contact") + "#contact-form")

        # 3. Extract form data (supports both standard form POST and JSON fetch)
        if request.is_json:
            payload = request.get_json(silent=True) or {}
            name = payload.get("name", "").strip()
            email = payload.get("email", "").strip()
            subject = payload.get("subject", "").strip()
            message = payload.get("message", "").strip()
            honeypot = payload.get("website", "").strip()
        else:
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            subject = request.form.get("subject", "").strip()
            message = request.form.get("message", "").strip()
            honeypot = request.form.get("website", "").strip()

        # 4. Anti-spam honeypot detection
        if honeypot:
            logger.warning("Spam bot trapped by honeypot field from IP: %s", client_ip)
            # Pretend success to bot without doing work
            if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": True, "message": "Message received."}), 200
            flash("Thank you for reaching out!", "success")
            return redirect(url_for("contact"))

        # 5. Server-side Input Validation
        errors = []
        if not name or len(name) < 2 or len(name) > 100:
            errors.append("Please enter a valid name (2 to 100 characters).")

        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not email or len(email) > 120 or not re.match(email_regex, email):
            errors.append("Please provide a valid email address.")

        if subject and len(subject) > 150:
            errors.append("Subject cannot exceed 150 characters.")

        if not message or len(message) < 10 or len(message) > 3000:
            errors.append("Message must be between 10 and 3,000 characters.")

        if errors:
            combined_error = " ".join(errors)
            if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "message": combined_error, "errors": errors}), 400
            for err in errors:
                flash(err, "error")
            return redirect(url_for("contact") + "#contact-form")

        # 6. Delivery Processing (Safe local testing vs Configured SMTP)
        mail_server = app.config.get("MAIL_SERVER")
        mail_username = app.config.get("MAIL_USERNAME")
        recipient = app.config.get("CONTACT_RECIPIENT_EMAIL")

        if mail_server and mail_username:
            try:
                # Dispatch email via configured SMTP (e.g. AWS SES SMTP or Gmail)
                msg = MIMEMultipart()
                msg["From"] = app.config.get("MAIL_DEFAULT_SENDER")
                msg["To"] = recipient
                msg["Reply-To"] = email
                msg["Subject"] = f"[Portfolio Contact] {subject or 'New Inquiry from ' + name}"

                body = (
                    f"New message from your portfolio contact form:\n\n"
                    f"Name: {name}\n"
                    f"Email: {email}\n"
                    f"Subject: {subject or 'N/A'}\n"
                    f"IP Address: {client_ip}\n"
                    f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
                    f"Message:\n{message}\n"
                )
                msg.attach(MIMEText(body, "plain"))

                with smtplib.SMTP(mail_server, app.config.get("MAIL_PORT", 587)) as server:
                    if app.config.get("MAIL_USE_TLS"):
                        server.starttls()
                    server.login(mail_username, app.config.get("MAIL_PASSWORD", ""))
                    server.send_message(msg)

                success_msg = "Thank you! Your message has been sent successfully. I will get back to you shortly."
                logger.info("Email successfully dispatched for contact from %s", email)

            except Exception as e:
                # Do not claim message was delivered if email failed
                logger.error("SMTP dispatch failed: %s", str(e))
                delivery_err = "The email service encountered a transmission error. Please reach out directly at benarjip69@gmail.com."
                if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify({"success": False, "message": delivery_err}), 502
                flash(delivery_err, "error")
                return redirect(url_for("contact") + "#contact-form")
        else:
            # Safe local development mode: log message safely without exposing secrets
            logger.info(
                "[LOCAL DEV CONTACT SUBMISSION]\nFrom: %s <%s>\nSubject: %s\nIP: %s\nMessage:\n%s",
                name,
                email,
                subject or "(None)",
                client_ip,
                message,
            )
            success_msg = (
                "Thank you, " + name + "! Your message was received in development testing mode. "
                "In production, this routes via API Gateway, Lambda, and Amazon SES."
            )

        if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": True, "message": success_msg}), 200

        flash(success_msg, "success")
        return redirect(url_for("contact") + "#contact-form")

    @app.route("/resume")
    def resume():
        """Serve or download verified resume PDF."""
        resume_path = BASE_DIR / "static" / "files" / "resume.pdf"
        if not resume_path.is_file():
            abort(404, description="Resume file not found.")

        # Determine if user requested attachment download or inline view
        as_attachment = request.args.get("download", "0").lower() in ("1", "true", "yes")

        return send_file(
            resume_path,
            mimetype="application/pdf",
            as_attachment=as_attachment,
            download_name="P_Benarji_Rathnam_Resume.pdf",
        )

    @app.route("/health")
    def health():
        """Health check endpoint for AWS App Runner, ALB, or monitoring."""
        return jsonify(
            {
                "status": "healthy",
                "service": "benarji-portfolio",
                "version": "1.0.0",
                "timestamp": datetime.now().isoformat(),
                "environment": app.config.get("ENV", config_name),
            }
        ), 200

    # -------------------------------------------------------------
    # Error Handlers
    # -------------------------------------------------------------

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html", profile=PROFILE), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error("Internal Server Error: %s", str(error))
        return render_template("500.html", profile=PROFILE), 500

    return app


# Create default application instance for direct running & WSGI servers
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1")
    app.run(host="0.0.0.0", port=port, debug=debug)
