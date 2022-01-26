from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def sent_verification_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        "Код подтверждения",
        f"Ваш код: {confirmation_code}",
        settings.ADMIN_EMAIL,
        [user.email],
        fail_silently=False,
    )
