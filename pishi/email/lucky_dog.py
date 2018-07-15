from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from ..models import User


def send_notification():
    #for user in User.objects.all():
    user= User.objects.get(username='rahiminasab')
    if user.email and user.is_active:
        subject = 'Introducing Lucky Dog winner concept'
        message = render_to_string('email/lucky_dog/email_string.html', {
            'user': user,
            'domain': 'www.piishi.com'
        })
        print('going to email ', user.email)
        EmailMessage(
            subject, message, to=[user.email]
        ).send()