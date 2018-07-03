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
# match = Match.objects.get(id=55)
#
# predictions = match.predictions.all()
# print 'num predicts before=', len(predictions)
# for predict in predictions:
#     score = Score.objects.get(match_set=match.match_set, user=predict.user)
#     score.num_predicted -= 1
#     score.value -= predict.value()
#     score.save()
#
# match.finished = False
# match.exceptional_badge = None
# match.winner = match.get_winner_in_120()
# match.summary.royals = 0
# match.summary.full_houses = 0
# match.summary.straights = 0
# match.summary.one_pairs = 0
# match.summary.oracles = 0
# match.summary.trelawneies = 0
# match.summary.nostradamuses = 0
# match.summary.save()
# match.save()
#
# predictions = match.predictions.all()
# print 'num predicts after=', len(predictions)
# for predict in predictions:
#     predict.normal_badge = None
#     predict.exceptional_badge = None
#     predict.penalty_badge = False
#     predict.winner = predict.get_winner_in_120()
#     predict.save()
#
# match.finished = True
# match.save()
