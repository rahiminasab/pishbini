from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse

from ..forms import SignUpForm, EmailReqForm
from ..models import User

from tokens import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            email = form.cleaned_data.get('email')
            user.save()

            send_activation_email(request, user, email)
            return redirect('/pending_activation/%s'%email)
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def pending_activation(request, email):
    return render(request, 'registration/pending_activation.html', {"email": email})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'registration/activation_done.html')
    else:
        return HttpResponse('Activation link is invalid!')


def email_req(request):
    user = request.user
    if request.method == 'POST':
        form = EmailReqForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email_input')
            user.is_active = False
            user.email = email
            user.save()

            send_activation_email(request, user, email)
            return redirect('/pending_activation/%s'%email)
    else:
        form = EmailReqForm()
    return render(request, 'registration/email_required.html', {'form': form})


def send_activation_email(request, user, to_email_address):
    subject = 'Please activate your account at Piishi.com'
    message = render_to_string('registration/acc_active_email.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    EmailMessage(
        subject, message, to=[to_email_address]
    ).send()