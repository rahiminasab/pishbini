from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

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
    winner = models.ForeignKey(Team, null=True, blank=True)
    rare_extra = models.IntegerField(default=-1)
    is_past = False

    @property
    def due(self):
        return datetime.now(pytz.UTC) >= self.date

    def get_winner(self):
        if self.home_result > self.away_result:
            return self.home_team
        elif self.home_result == self.away_result == 0:
            if not self.home_penalty and not self.away_penalty:
                return None
            elif self.home_penalty > self.away_penalty:
                return self.home_team
            else:
                return self.away_team
        elif self.home_result == self.away_result:
            return None
        else:
            return self.away_team

    def save(self, *args, **kwargs):
        if self.finished and self.rare_extra == -1:
            self.winner = self.get_winner()
            tot_count = Predict.objects.filter(match=self).count()
            if tot_count > 0:
                err_count = Predict.objects.filter(match=self).exclude(winner=self.winner).count()
                p_val = (tot_count-err_count)/float(tot_count)
                if p_val < 0.05:
                    self.rare_extra = 20
                elif p_val < 0.1:
                    self.rare_extra = 15
                elif p_val < 0.15:
                    self.rare_extra = 10
                else:
                    self.rare_extra = 0
            else:
                self.rare_extra = 0

            super(Match, self).save(*args, **kwargs)
            Score.update_scores_for(self)
        else:
            super(Match, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s vs %s"%(self.home_team, self.away_team)


class Predict(models.Model):
    user = models.ForeignKey(User, related_name="predictions", on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    home_result_predict = models.PositiveIntegerField()
    away_result_predict = models.PositiveIntegerField()
    home_penalty_predict = models.PositiveIntegerField(null=True, blank=True)
    away_penalty_predict = models.PositiveIntegerField(null=True, blank=True)
    winner = models.ForeignKey(Team, null=True, blank=False)

    class Meta:
        unique_together = ('user', 'match',)

    def get_winner(self):
        if self.home_result_predict > self.away_result_predict:
            return self.match.home_team
        elif self.home_result_predict == self.away_result_predict == 0:
            if not self.home_penalty_predict and not self.away_penalty_predict:
                return None
            elif self.home_penalty_predict > self.away_penalty_predict:
                return self.match.home_team
            else:
                return self.match.away_team
        elif self.home_result_predict == self.away_result_predict:
            return None
        else:
            return self.match.away_team

    def value(self):
        def is_royal_flush():
            if self.home_result_predict == self.match.home_result and self.away_result_predict == self.match.away_result:
                if self.match.home_penalty:
                    return self.home_penalty_predict == self.match.home_penalty
                return True
            return False

        def is_full_house():
            return self.home_result_predict-self.away_result_predict == self.match.home_result-self.match.away_result

        if not self.match.finished:
            return 0

        if self.winner == self.match.winner:
            if is_royal_flush():
                val = 20
            elif is_full_house():
                val = 12
            else:
                val = 8
            val += self.match.rare_extra
        else:
            val = 2

        return val

    def save(self, *args, **kwargs):
        self.winner = self.get_winner()
        super(Predict, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s-%s: %s-%s"%(self.user, self.match, self.home_result_predict, self.away_result_predict)


class Score(models.Model):
    user = models.OneToOneField(User, related_name="score", on_delete=models.CASCADE)
    value = models.FloatField(default=0)
    num_predicted = models.PositiveIntegerField(default=0)

    @property
    def normalized_value(self):
        return (self.value/self.num_predicted)*(self.num_predicted**0.2)

    @staticmethod
    def update_scores_for(match):
        predicts = Predict.objects.filter(match=match)
        for predict in predicts:
            try:
                score_obj = Score.objects.get(user=predict.user)
                score_obj.num_predicted += 1
            except Score.DoesNotExist:
                score_obj = Score(user=predict.user, num_predicted=1)
            score_obj.value += predict.value()
            score_obj.save()

    def __unicode__(self):
        return "%s: %s" % (self.user, self.value)