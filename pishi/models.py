from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from datetime import datetime
import pytz

from badge import *


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
    ROUND16 = 1
    ROUND8 = 2
    ROUND4 = 3
    ROUND2_LOSER = 4
    ROUND2 = 5
    MATCH_TYPES = (
        (GROUP, "Group"),
        (ROUND16, "Round of 16"),
        (ROUND8, "Quarter Finals"),
        (ROUND4, "Semi Finals"),
        (ROUND2_LOSER, "Third Place play-off"),
        (ROUND2, "Final")
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
    winner = models.ForeignKey(Team, null=True, blank=True)
    exceptional_badge = models.PositiveIntegerField(choices=Badge.exceptional_types, null=True, blank=True)
    summary = models.OneToOneField("MatchSummary", related_name="match", on_delete=models.CASCADE, null=True, blank=True)

    @property
    def due(self):
        return datetime.now(pytz.UTC) >= self.date

    def get_winner(self):
        if self.home_result > self.away_result:
            return self.home_team
        elif self.home_result == self.away_result:
            if not self.home_penalty:
                return None
            elif self.home_penalty > self.away_penalty:
                return self.home_team
            else:
                return self.away_team
        else:
            return self.away_team

    def save(self, *args, **kwargs):
        if self.finished and not self.exceptional_badge:
            self.winner = self.get_winner()
            tot_count = Predict.objects.filter(match=self).count()
            if tot_count > 0:
                err_count = Predict.objects.filter(match=self).exclude(winner=self.winner).count()
                p_val = (tot_count-err_count)/float(tot_count)
                if p_val < 0.2:
                    self.exceptional_badge = Badge.ORACLE
                elif p_val < 0.3:
                    self.exceptional_badge = Badge.NOSTRADAMUS
                elif p_val < 0.4:
                    self.exceptional_badge = Badge.TRELAWNEY
                else:
                    self.exceptional_badge = Badge.NOTHING
            else:
                self.exceptional_badge = Badge.NOTHING

            self.summary = MatchSummary.objects.create()

            super(Match, self).save(*args, **kwargs)

            Predict.update_predictions_for(self)
        else:
            super(Match, self).save(*args, **kwargs)

    @property
    def encoded_id(self):
        return urlsafe_base64_encode(force_bytes(self.pk))

    @staticmethod
    def decode_id(encoded_id):
        return urlsafe_base64_decode(encoded_id)

    def __unicode__(self):
        return "%s vs %s"%(self.home_team, self.away_team)


class MatchSummary(models.Model):
    royals = models.PositiveIntegerField(default=0)
    full_houses = models.PositiveIntegerField(default=0)
    straights = models.PositiveIntegerField(default=0)
    one_pairs = models.PositiveIntegerField(default=0)
    oracles = models.PositiveIntegerField(default=0)
    nostradamuses = models.PositiveIntegerField(default=0)
    trelawneies = models.PositiveIntegerField(default=0)


class Predict(models.Model):
    user = models.ForeignKey(User, related_name="predictions", on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    home_result = models.PositiveIntegerField()
    away_result = models.PositiveIntegerField()
    home_penalty = models.PositiveIntegerField(null=True, blank=True)
    away_penalty = models.PositiveIntegerField(null=True, blank=True)
    winner = models.ForeignKey(Team, null=True, blank=False)
    normal_badge = models.PositiveIntegerField(choices=Badge.normal_types, null=True, blank=True)
    exceptional_badge = models.PositiveIntegerField(choices=Badge.exceptional_types, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'match',)

    def get_winner(self):
        if self.home_result > self.away_result:
            return self.match.home_team
        elif self.home_result == self.away_result:
            if not self.home_penalty:
                return None
            elif self.home_penalty > self.away_penalty:
                return self.match.home_team
            else:
                return self.match.away_team
        else:
            return self.match.away_team

    def is_royal(self):
        if self.home_result == self.match.home_result and self.away_result == self.match.away_result:
            if self.match.home_penalty:
                return self.home_penalty == self.match.home_penalty
            return True
        return False

    def is_full_house(self):
        return self.home_result - self.away_result == self.match.home_result - self.match.away_result

    def is_straight(self):
        return self.winner == self.match.winner

    def value(self):
        if not self.match.finished:
            return 0
        return Badge.get_value(self.normal_badge) + Badge.get_value(self.exceptional_badge)

    def save(self, *args, **kwargs):
        if self.home_result != self.away_result:
            self.home_penalty = None
            self.away_penalty = None

        if not self.normal_badge and self.match.finished:
            self.winner = self.get_winner()
            if self.is_royal():
                self.normal_badge = Badge.ROYAL
                self.match.summary.royals += 1
            elif self.is_full_house():
                self.normal_badge = Badge.FULL_HOUSE
                self.match.summary.full_houses += 1
            elif self.is_straight():
                self.normal_badge = Badge.STRAIGHT
                self.match.summary.straights += 1
            else:
                self.normal_badge = Badge.ONE_PAIR
                self.match.summary.one_pairs += 1

            if self.is_straight():
                self.exceptional_badge = self.match.exceptional_badge
                if self.exceptional_badge == Badge.ORACLE:
                    self.match.summary.oracles += 1
                elif self.exceptional_badge == Badge.NOSTRADAMUS:
                    self.match.summary.nostradamuses += 1
                elif self.exceptional_badge == Badge.TRELAWNEY:
                    self.match.summary.trelawneies += 1
            self.match.summary.save()

        super(Predict, self).save(*args, **kwargs)

    @staticmethod
    def update_predictions_for(match):
        predictions = Predict.objects.filter(match=match)
        for predict in predictions:
            predict.save()
            try:
                score_obj = Score.objects.get(user=predict.user)
                score_obj.num_predicted += 1
            except Score.DoesNotExist:
                score_obj = Score(user=predict.user, num_predicted=1)
            score_obj.value += predict.value()
            score_obj.save()

    def __unicode__(self):
        return "%s-%s: %s-%s"%(self.user, self.match, self.home_result, self.away_result)


class Score(models.Model):
    user = models.OneToOneField(User, related_name="score", on_delete=models.CASCADE)
    value = models.FloatField(default=0)
    num_predicted = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return "%s: %s" % (self.user, self.value)