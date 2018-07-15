from django.shortcuts import render
from ..models import *


def render_profile(request, username):
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return render(request, '404.html')

    return render(request, 'profile/profile_main.html', {"profile": profile})