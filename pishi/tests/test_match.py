from django.test import TestCase
import datetime
from pytz import UTC

from pishi.models import Team, Match, MatchSet, User, Score
from pishi.badge import *


class MatchTestCase(TestCase):
    fixtures = ['users.json', 'teams.json', 'matchsets.json', 'matchset_summary.json', 'matches_r16.json',
                'predictions_oracle.json', 'predictions_nostradamus.json', 'predictions_trelawney.json']

    def setUp(self):
        match_sets = MatchSet.objects.all()
        users = User.objects.all()
        for u in users:
            for ms in match_sets:
                Score.objects.create(match_set=ms, user=u)

    def test_creation(self):
        with self.assertRaises(Match.DoesNotExist):
            match = Match.objects.get(match_set=1, home_team=9, away_team=18)
        match = Match.objects.create(match_set_id=1, home_team_id=9, away_team_id=18, type=Match.ROUND16,
                                     date="2018-06-30T17:00:00+03:00")
        self.assertEqual(match.home_team.name, "France")
        self.assertEqual(match.away_team.name, "Switzerland")

    def test_due(self):
        match = Match.objects.get(id=49)
        self.assertTrue(match.due)
        match.date = datetime.datetime.now(UTC) + datetime.timedelta(days=1)
        self.assertFalse(match.due)

    def test_winner_in_120(self):
        match = Match.objects.get(id=49)

        match.home_result = 0
        match.away_result = 1
        self.assertEqual(match.get_winner_in_120(), match.away_team)
        self.assertIsNone(match.get_winner_in_penalty())

        match.home_result = 2
        match.away_result = 1
        self.assertEqual(match.get_winner_in_120(), match.home_team)
        self.assertIsNone(match.get_winner_in_penalty())

        match.home_result = 0
        match.away_result = 0
        self.assertIsNone(match.get_winner_in_120())

        match.home_result = 1
        match.away_result = 1
        self.assertIsNone(match.get_winner_in_120())

    def test_has_penalty(self):
        match = Match.objects.get(id=49)

        match.home_result = 1
        match.away_result = 0
        match.home_penalty = 0
        match.away_penalty = 0
        self.assertFalse(match.has_penalty())

        match.home_result = 0
        match.away_result = 0
        match.home_penalty = 1
        match.away_penalty = 0
        self.assertTrue(match.has_penalty())

    def test_winner_in_penalty(self):
        match = Match.objects.get(id=49)
        match.home_result = 0
        match.away_result = 0

        with self.assertRaises(ValueError):
            match.get_winner_in_penalty()
        match.home_penalty = 1
        with self.assertRaises(ValueError):
            match.get_winner_in_penalty()
        match.away_penalty = 3
        self.assertEqual(match.away_team, match.get_winner_in_penalty())
        match.home_penalty = 4
        self.assertEqual(match.home_team, match.get_winner_in_penalty())
        match.home_penalty = 3
        with self.assertRaises(ValueError):
            match.get_winner_in_penalty()

    def test_exceptional_badge_NOTHING(self):
        match = Match.objects.get(id=49)
        self.assertIsNone(match.exceptional_badge)
        match.finished = True
        match.assign_exceptional_badge()
        self.assertEqual(match.exceptional_badge, Badge.NOTHING)

    def test_exceptional_badge_ORACLE(self):
        match = Match.objects.get(id=50)
        self.assertIsNone(match.exceptional_badge)
        match.home_result = 1
        match.away_result = 3
        match.save()
        self.assertIsNone(match.exceptional_badge)
        match.finished = True
        match.save()
        self.assertEqual(match.exceptional_badge, Badge.ORACLE)

    def test_exceptional_badge_NOSTRADAMUS(self):
        match = Match.objects.get(id=51)
        self.assertIsNone(match.exceptional_badge)
        match.home_result = 1
        match.away_result = 3
        match.save()
        self.assertIsNone(match.exceptional_badge)
        match.finished = True
        match.save()
        self.assertEqual(match.exceptional_badge, Badge.NOSTRADAMUS)

    def test_exceptional_badge_TRELAWNEY(self):
        match = Match.objects.get(id=52)
        self.assertIsNone(match.exceptional_badge)
        match.home_result = 1
        match.away_result = 3
        match.save()
        self.assertIsNone(match.exceptional_badge)
        match.finished = True
        match.save()
        self.assertEqual(match.exceptional_badge, Badge.TRELAWNEY)
