from django.conf.urls import url

import views as match_views


urlpatterns = [
    url(r'^match-set/(?P<match_set_id>[0-9A-Za-z_\-]+)', match_views.render_matches, name='render_matches'),
    url(r'^predict/(?P<match_id>[0-9A-Za-z_\-]+)/$', match_views.submit_prediction, name='submit_prediction'),
]
