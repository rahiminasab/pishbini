from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie

from models import *


@ensure_csrf_cookie
def index(request):
    return home(request)


def home(request):
    user = request.user

    if not user.is_authenticated():
        return HttpResponseRedirect(reverse("login"))

    if not user.email or not user.is_active:
        import registrar.views as registrar
        return registrar.user_activation_required(request)

    match_sets = MatchSet.objects.filter(finished=False).all()

    return render(request, "index.html", {"match_sets": match_sets})


def rules(request):
    return render(request, "rules.html")
