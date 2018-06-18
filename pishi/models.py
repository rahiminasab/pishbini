from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=50)
    rank = models.PositiveIntegerField()
    fifa_code = models.CharField(max_length=10, null=True)
    iso2 = models.CharField(max_length=3, null=True)
    flag = models.URLField(null=True)
    emoji = models.CharField(max_length=20, null=True)
    emoji_string = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return self.name


class Match(models.Model):
    GROUP = 0
    KNOCKOUT = 1
    MATCH_TYPES = (
        (GROUP, "Group"),
        (KNOCKOUT, "Knock out")
    )
    type = models.PositiveIntegerField(choices=MATCH_TYPES)
    home_team = models.ForeignKey(Team, related_name="home_team", on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name="away_team", on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    home_result = models.PositiveIntegerField(null=True, blank=True)
    away_result = models.PositiveIntegerField(null=True, blank=True)
    home_penalty = models.PositiveIntegerField(null=True, blank=True)
    away_penalty = models.PositiveIntegerField(null=True, blank=True)
    finished = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s vs %s"%(self.home_team, self.away_team)


class Predict(models.Model):
    user = models.ForeignKey(User, related_name="predictions", on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    home_result_predict = models.PositiveIntegerField()
    away_result_predict = models.PositiveIntegerField()
    home_penalty_predict = models.PositiveIntegerField(null=True, blank=True)
    away_penalty_predict = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        return "%s-%s"%(self.home_result_predict, self.away_result_predict)