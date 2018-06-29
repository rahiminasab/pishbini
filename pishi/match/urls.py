from django.conf.urls import url

import views as match_views


urlpatterns = [
    url(r'^match-set/(?P<match_set_id>[0-9A-Za-z_\-]+)', match_views.render_matches, name='render_matches'),
    url(r'^predict/(?P<match_id>[0-9A-Za-z_\-]+)/$', match_views.submit_prediction, name='submit_prediction'),
]

# from ..models import *
#
# m_set = MatchSet.objects.get(id=1)
# srs = MatchSummary.objects.all()
# m_set.summary = MatchSetSummary()
# for s in srs:
#     m_set.summary.royals += s.royals
#     m_set.summary.full_houses += s.full_houses
#     m_set.summary.straights += s.straights
#     m_set.summary.one_pairs += s.one_pairs
#
# m_set.summary.save()