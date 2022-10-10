from string import ascii_letters, digits
from  random import choices

from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.core.mail import send_mail
from django.conf import settings



def get_random_string(count: int) -> str:
    return ''.join(choices(ascii_letters + digits, k=count))
    

def send_client_approval_mail(msg: str, subject: str, email: str) -> None:

    settings.configure(EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend')
    send_mail(
        f'{subject}',
        f'{msg}',
        'usmilitiapride@zohomail.com',
        [f'{email}'],
        fail_silently=False,
    )


if __name__ == '__main__':
    print(get_random_string(6))

    msg = "Just testing"
    subject = "working working working"
    email = "ighotagaddiel98@gmail.com"
    send_client_approval_mail(msg=msg, subject=subject, email=email)