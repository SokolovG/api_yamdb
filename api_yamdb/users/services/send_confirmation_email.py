from django.core.mail import send_mail

from .generate_confirmation_code import code_generator
from ..constants import EMAIL_SUBJECT, EMAIL_MESSAGE


class SendConfirmationCode:

    def send_mail(self, email: str) -> None:
        code = code_generator.generate()
        send_mail(
            subject=EMAIL_SUBJECT,
            message=f'{EMAIL_MESSAGE}{code}',
            from_email='YaReviewApp@example.com',
            recipient_list=[email],
            fail_silently=False
        )
