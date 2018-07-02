"""pishbini URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from pishi import views as core_views
from pishi.registrar import urls as registrar_urls
from pishi.match import urls as match_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', core_views.index),
    url(r'^home/$', core_views.home, name='home'),
    url(r'^rules/$', core_views.rules, name='rules')
]

urlpatterns.extend(registrar_urls.urlpatterns)
urlpatterns.extend(match_urls.urlpatterns)

# from pishi.models import *
# matches = Match.objects.filter(date__range=["2018-06-30", "2018-07-02"])
# for match in matches:
#     print 'num predicts before=', len(match.predictions.all())
#     match.finished = False
#     match.exceptional_badge = None
#     match.winner = match.get_winner_in_120()
#     match.match_set.summary.royals -= match.summary.royals
#     match.match_set.summary.full_houses -= match.summary.full_houses
#     match.match_set.summary.straights -= match.summary.straights
#     match.match_set.summary.one_pairs -= match.summary.one_pairs
#     match.match_set.summary.save()
#     match.summary.royals = 0
#     match.summary.full_houses = 0
#     match.summary.straights = 0
#     match.summary.one_pairs = 0
#     match.summary.oracles = 0
#     match.summary.trelawneies = 0
#     match.summary.nostradamuses = 0
#     match.summary.save()
#     match.save()
#     predictions = match.predictions.all()
#     print 'num predicts after=', len(predictions)
#     for prediction in predictions:
#         prediction.normal_badge = None
#         prediction.exceptional_badge = None
#         prediction.penalty_badge = False
#         prediction.winner = prediction.get_winner_in_120()
#         prediction.save()
#
#         score = Score.objects.get(match_set=match.match_set, user=prediction.user)
#         score.num_predicted -= 1
#         score.save()
#
# for score in Score.objects.all():
#     score.value = 0
#     score.save()
# #
# for match in matches:
#     match.finished = True
#     match.save()

