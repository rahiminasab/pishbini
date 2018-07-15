from django.conf.urls import url

import views as profile_views

urlpatterns = [
    url(r'^user/(?P<username>.+)', profile_views.render_profile, name='profile'),
]