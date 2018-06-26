from django.conf.urls import url

import views as match_views


urlpatterns = [
    url(r'^predict/', match_views.submit_prediction, name='submit_prediction'),
]
