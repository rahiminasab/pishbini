from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from datetime import datetime
import pytz


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
    is_past = False

    @property
    def due(self):
        return datetime.now(pytz.UTC) >= self.date

    def winner(self):
        if self.home_result > self.away_result:
            return self.home_team
        elif self.home_result == self.away_result == 0:
            if self.home_penalty > self.away_penalty:
                return self.home_team
            else:
                return self.away_team
        else:
            return self.away_team

    def __unicode__(self):
        return "%s vs %s"%(self.home_team, self.away_team)


class Predict(models.Model):
    user = models.ForeignKey(User, related_name="predictions", on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    home_result_predict = models.PositiveIntegerField()
    away_result_predict = models.PositiveIntegerField()
    home_penalty_predict = models.PositiveIntegerField(null=True, blank=True)
    away_penalty_predict = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'match',)

    def winner(self):
        if self.home_result_predict > self.away_result_predict:
            return self.match.home_team
        elif self.home_result_predict == self.away_result_predict == 0:
            if self.home_penalty_predict > self.away_penalty_predict:
                return self.match.home_team
            else:
                return self.match.away_team
        else:
            return self.match.away_team

    def value(self):
        if not self.match.finished:
            return 0
        val = 0
        if self.home_result_predict == self.match.home_result and self.away_result_predict == self.match.away_result:
            val += 20
        elif self.winner() == self.match.winner():
            val += 5
            if self.home_result_predict-self.away_result_predict == self.match.home_result-self.match.away_result:
                val += 8
        return val



    def __unicode__(self):
        return "%s-%s: %s-%s"%(self.user, self.match, self.home_result_predict, self.away_result_predict)


class Score(models.Model):
    user = models.OneToOneField(User, related_name="score", on_delete=models.CASCADE)
    value = models.FloatField()
    last_time_calculated = models.DateTimeField(auto_now_add=True)

    def calc(self):
        predictions = self.user.predictions.all()
        score = 0
        for prediction in predictions:
            score += prediction.value()
        return score

    def __unicode__(self):
        return "%s: %s" % (self.user, self.value)