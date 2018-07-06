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


class MatchSet(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)
    finished = models.BooleanField(default=False)
    winner = models.ForeignKey(Team, null=True, blank=True)
    flag = models.URLField(null=True)
    summary = models.OneToOneField("MatchSetSummary", related_name="match_set", on_delete=models.CASCADE, null=True,
                                   blank=True)

    @property
    def encoded_id(self):
        return urlsafe_base64_encode(force_bytes(self.pk))

    @staticmethod
    def decode_id(encoded_id):
        return urlsafe_base64_decode(encoded_id)

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
    match_set = models.ForeignKey(MatchSet, related_name="matches", on_delete=models.CASCADE)
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
    summary = models.OneToOneField("MatchSummary", related_name="match",
                                   on_delete=models.CASCADE, null=True, blank=True)

    @property
    def due(self):
        return datetime.now(pytz.UTC) >= self.date

    def get_winner_in_120(self):
        if self.home_result > self.away_result:
            return self.home_team
        elif self.home_result == self.away_result:
            return None
        else:
            return self.away_team

    def has_penalty(self):
        if self.get_winner_in_120():
            return False
        return self.home_penalty is not None and self.away_penalty is not None

    def get_winner_in_penalty(self):
        if self.get_winner_in_120():
            return None
        if not self.has_penalty():
            raise ValueError("Match %s, does not lead into penalties, but you have requested for penalties." % self)
        if self.home_penalty == self.away_penalty:
            raise ValueError("Match %s, cannot lead to equal penalty points." % self)
        elif self.home_penalty > self.away_penalty:
            return self.home_team
        else:
            return self.away_team

    def assign_exceptional_badge(self):
        if not self.finished:
            return
        tot_count = self.predictions.count()
        if tot_count > 0:
            true_count = self.predictions.filter(winner=self.winner).count()
            p_val = true_count / float(tot_count)
            if p_val <= BadgeProbability.ORACLE:
                self.exceptional_badge = Badge.ORACLE
            elif p_val <= BadgeProbability.NOSTRADAMUS:
                self.exceptional_badge = Badge.NOSTRADAMUS
            elif p_val <= BadgeProbability.TRELAWNEY:
                self.exceptional_badge = Badge.TRELAWNEY
            else:
                self.exceptional_badge = Badge.NOTHING
        else:
            self.exceptional_badge = Badge.NOTHING

    def is_concluded(self):
        return self.exceptional_badge is not None

    def conclude(self):
        if not self.finished or self.is_concluded():
            return
        self.winner = self.get_winner_in_120()
        self.assign_exceptional_badge()
        if self.summary is None or not self.summary.pk:
            self.summary = MatchSummary.objects.create()
        self.save()
        Predict.conclude_predictions(self)

    def save(self, *args, **kwargs):
        if self.finished:
            if self.home_result is None or self.away_result is None:
                raise ValueError("You cannot know who is winner of the match %s "
                                 "while you didn't input the final results" % self)
            if not self.is_concluded():
                self.conclude()
        super(Match, self).save(*args, **kwargs)

    @property
    def encoded_id(self):
        return urlsafe_base64_encode(force_bytes(self.pk))

    @staticmethod
    def decode_id(encoded_id):
        return urlsafe_base64_decode(encoded_id)

    def __unicode__(self):
        return "%s vs %s" % (self.home_team, self.away_team)


class MatchSummary(models.Model):
    royals = models.PositiveIntegerField(default=0)
    full_houses = models.PositiveIntegerField(default=0)
    straights = models.PositiveIntegerField(default=0)
    one_pairs = models.PositiveIntegerField(default=0)
    oracles = models.PositiveIntegerField(default=0)
    nostradamuses = models.PositiveIntegerField(default=0)
    trelawneies = models.PositiveIntegerField(default=0)

    def delete(self, *args, **kwargs):
        self.match.match_set.summary.royals -= self.royals
        self.match.match_set.summary.full_houses -= self.full_houses
        self.match.match_set.summary.straights -= self.straights
        self.match.match_set.summary.one_pairs -= self.one_pairs
        super(MatchSummary, self).delete(*args, **kwargs)


class MatchSetSummary(models.Model):
    royals = models.PositiveIntegerField(default=0)
    full_houses = models.PositiveIntegerField(default=0)
    straights = models.PositiveIntegerField(default=0)
    one_pairs = models.PositiveIntegerField(default=0)


class Predict(models.Model):
    user = models.ForeignKey(User, related_name="predictions", on_delete=models.CASCADE)
    match = models.ForeignKey(Match, related_name="predictions", on_delete=models.CASCADE)
    home_result = models.PositiveIntegerField()
    away_result = models.PositiveIntegerField()
    home_penalty = models.PositiveIntegerField(null=True, blank=True)
    away_penalty = models.PositiveIntegerField(null=True, blank=True)
    winner = models.ForeignKey(Team, null=True, blank=False)
    normal_badge = models.PositiveIntegerField(choices=Badge.normal_types, null=True, blank=True)
    penalty_badge = models.BooleanField(default=False, blank=True)
    exceptional_badge = models.PositiveIntegerField(choices=Badge.exceptional_types, null=True, blank=True)
    concluded = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'match',)

    def get_winner_in_120(self):
        if self.home_result is None or self.away_result is None:
            raise ValueError("You cannot know who is winner of the predict %s "
                             "while you didn't input the final results" % self)

        if self.home_result > self.away_result:
            return self.match.home_team
        elif self.home_result == self.away_result:
            return None
        else:
            return self.match.away_team

    def has_penalty(self):
        return self.home_penalty is not None and self.away_penalty is not None

    def get_winner_in_penalty(self):
        if self.get_winner_in_120():
            return None
        if not self.has_penalty():
            raise ValueError("Prediction %s, does not include penalties, but you have requested for penalties." % self)
        if self.home_penalty == self.away_penalty:
            raise ValueError("Prediction %s, cannot lead to equal penalty points." % self)

        if self.home_penalty > self.away_penalty:
            return self.match.home_team
        else:
            return self.match.away_team

    def is_royal(self):
        if not self.match.finished:
            raise TypeError("match %s is not finished yet, so we cannot tell if %s is royal!" % (self.match, self))
        return self.home_result == self.match.home_result and self.away_result == self.match.away_result

    def is_full_house(self):
        if not self.match.finished:
            raise TypeError("match %s is not finished yet, so we cannot tell if %s is full house!" % (self.match, self))
        if self.is_straight():
            return self.home_result - self.away_result == self.match.home_result - self.match.away_result
        return False

    def is_straight(self):
        if not self.match.finished:
            raise TypeError("match %s is not finished yet, so we cannot tell if %s is straight!" % (self.match, self))
        return self.winner == self.match.winner

    def value(self):
        if not self.concluded:
            return 0
        return Badge.get_value(self.normal_badge) + Badge.get_value(self.exceptional_badge) + \
               (BadgeScore.PENALTY if self.penalty_badge else 0)

    def assign_normal_badge(self):
        if not self.match.finished:
            return
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

    def assign_penalty_badge(self):
        if self.winner is not None or not self.match.has_penalty():
            return
        if self.get_winner_in_penalty() == self.match.get_winner_in_penalty():
            self.penalty_badge = True

    def assign_exceptional_badge(self):
        if not self.is_straight():
            self.exceptional_badge = Badge.NOTHING
            return

        self.exceptional_badge = self.match.exceptional_badge

        if self.exceptional_badge == Badge.ORACLE:
            self.match.summary.oracles += 1
        elif self.exceptional_badge == Badge.NOSTRADAMUS:
            self.match.summary.nostradamuses += 1
        elif self.exceptional_badge == Badge.TRELAWNEY:
            self.match.summary.trelawneies += 1

    def conclude(self):
        if self.concluded or not self.match.finished:
            return
        self.winner = self.get_winner_in_120()
        self.assign_normal_badge()
        self.assign_penalty_badge()
        self.assign_exceptional_badge()
        self.match.summary.save()
        self.concluded = True
        self.save()

        score_obj = Score.objects.get(user=self.user, match_set=self.match.match_set)
        score_obj.num_predicted += 1
        score_obj.value += self.value()
        score_obj.save()

    def save(self, *args, **kwargs):
        self.winner = self.get_winner_in_120()
        if not self.pk:
            if not Score.objects.filter(user=self.user, match_set=self.match.match_set).exists():
                Score.objects.create(user=self.user, match_set=self.match.match_set)

        super(Predict, self).save(*args, **kwargs)

    @staticmethod
    def conclude_predictions(finished_match):
        predictions = Predict.objects.filter(match=finished_match)
        for predict in predictions:
            predict.conclude()

        match_set_summary = finished_match.match_set.summary
        match_summary = finished_match.summary
        match_summary.refresh_from_db()
        match_set_summary.royals += match_summary.royals
        match_set_summary.full_houses += match_summary.full_houses
        match_set_summary.straights += match_summary.straights
        match_set_summary.one_pairs += match_summary.one_pairs
        match_set_summary.save()

    def __unicode__(self):
        return "%s-%s: %s-%s" % (self.user, self.match, self.home_result, self.away_result)


class Score(models.Model):
    match_set = models.ForeignKey(MatchSet, related_name="scores", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="scores", on_delete=models.CASCADE)
    value = models.FloatField(default=0)
    num_predicted = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('match_set', 'user')

    def __unicode__(self):
        return "%s: %s" % (self.user, self.value)
