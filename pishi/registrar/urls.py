from django.conf.urls import url
from django.contrib.auth import views as auth_views

import views as registrar_views


urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', registrar_views.signup, name='signup'),

    # ****** USER ACTIVATION URLs *******
    url(r'^user_activation_required/$', registrar_views.user_activation_required, name='user_activation_required'),
    url(r'^user_activation_pending/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$',
        registrar_views.user_activation_pending,
        name='user_activation_pending'),
    url(r'^user_activation_done/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        registrar_views.user_activation_done, name='user_activation_done'),

    # ****** RESET PASS URLs *******
    url(r'^reset_pass_submit/$',
        registrar_views.reset_pass_submit, name='reset_pass_submit'),
    url(r'^reset_pass_pending/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})$', registrar_views.reset_pass_pending,
        name='reset_pass_pending'),
    url(r'^reset_pass_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        registrar_views.reset_pass_confirm, name='reset_pass_confirm'),
    url(r'^reset_pass_done/', registrar_views.reset_pass_done, name='reset_pass_done')
]
