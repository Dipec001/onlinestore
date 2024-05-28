from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from .models import User, OneTimePassword
from django.core.validators import EmailValidator, validate_email
import pyotp
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)

def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), digits=6)
    return totp.now()

def send_otp_for_password_reset(email):
    try:
        # Validate email format
        validate_email(email)

        # Normalize email address (convert to lowercase)
        email = email.lower()
        
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValueError("No account associated with this email")
        
        # Delete any existing OTP for the user
        OneTimePassword.objects.filter(user=user).delete()

        otp_code = generate_otp()
        OneTimePassword.objects.create(user=user, code=otp_code)

        current_site = "Pharma"  # TODO: Get the site domain dynamically

        email_subject = "Password Reset OTP"
        email_body = f"Hello,\n\nYou're receiving this email because you requested a password reset for your account at {current_site}.\n\nYour one-time password (OTP) for password reset is: {otp_code} \n\nThis OTP is only valid for 10 minutes.\n\nIf you didn't request this, you can safely ignore this email.\n\nBest regards,\nThe {current_site} Team"



        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        email.send()

        logger.info('Test email sent successfully.')

        return True, "OTP sent successfully"  # Indicate that the OTP was sent successfully
    except User.DoesNotExist:
        return False, "User does not exist"
    except Exception as e:
        logger.error(f'Error sending email: {e}')
        error_message = f"An error occurred while sending OTP: {e}"
        return False, error_message  # Indicate that there was an error sending the OTP
