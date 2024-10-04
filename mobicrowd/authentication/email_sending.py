from django.core.mail import EmailMessage
from django.db import transaction
from django.template.loader import render_to_string

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from Mobicrowd_backend_project import settings
from mobicrowd.models.Users import Token


def send_verification_email(user):
    token_generator = PasswordResetTokenGenerator()
    with transaction.atomic():
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.delete()
            token = Token.objects.create(user=user)
        token.token = token_generator.make_token(user)
        token.save()
    verification_url = f'{settings.BASE_URL}/api/account_confirm_email/{user.pk}/{token.token}'
    subject = 'Verify your account'
    context = {
        'full_name': user.fullName,
        'verification_url': verification_url,
    }
    body = render_to_string('email_template', context)
    email = EmailMessage(subject=subject, body=body, from_email=settings.EMAIL_HOST_USER, to=[user.email])
    email.content_subtype = 'html'
    email.send()



