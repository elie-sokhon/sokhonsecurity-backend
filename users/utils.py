from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

def send_verification_email(request, user):
    """Send email verification link to the user"""
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # Detect if we're in local development
    if settings.DEBUG:
        protocol = "http"  # Local development uses HTTP
        domain = "127.0.0.1:8000"
    else:
        protocol = "https"  # Production uses HTTPS
        domain = "sokhonsecurity-backend-production.up.railway.app"

    verification_link = f"{protocol}://{domain}/api/verify-email/{uid}/{token}/"

    subject = "Verify Your Email - No Reply"
    message = f"Click the link below to verify your email:\n\n{verification_link}"

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

def build_frontend_link(path: str) -> str:
    """
    Builds a full frontend URL depending on the environment (localhost or production).
    Example: path = "reset-password/uid/token"
    """
    if settings.DEBUG:
        protocol = "http"
        domain = "localhost:3000"
    else:
        protocol = "https"
        domain = "www.sokhonsecurity.com"  # Change if you deploy frontend elsewhere

    return f"{protocol}://{domain}/{path}"