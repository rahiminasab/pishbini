from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from ..models import User, Match, Score


def send_semifinal_reminders():
    match = Match.objects.get(pk=61)
    for user in User.objects.all():
        try:
            score = Score.objects.get(user=user, match_set=match.match_set)
        except Score.DoesNotExist:
            print(user, 'not even scored')
            continue
        if not score.value > 0:
            print(user, 'not participated in round offs')
            continue
        if user.predictions.filter(match=match).exists():
            print(user, 'already has predicted')
            continue
        subject = 'Don\'t forget to predict!'
        message = render_to_string('email/reminders/email_string.html', {
            'user': user,
            'domain': 'www.piishi.com'
        })
        print('going to email ', user.email)
        EmailMessage(
            subject, message, to=[user.email]
        ).send()