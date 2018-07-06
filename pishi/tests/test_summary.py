from django.test import TestCase

from pishi.models import *


class SummaryTestCase(TestCase):
    fixtures = ['users.json', 'teams.json', 'matchsets.json', 'matchset_summary.json','match_and_predictions.json']
    
    def setUp(self):
        match_sets = MatchSet.objects.all()
        users = User.objects.all()
        for u in users:
            for ms in match_sets:
                Score.objects.create(match_set=ms, user=u)

        self.matchset = MatchSet.objects.get(pk=1)

        self.match_home_winner = Match.objects.get(pk=1)
        self.match_away_winner = Match.objects.get(pk=2)
        self.match_equal = Match.objects.get(pk=3)
        self.match_equal_0 = Match.objects.get(pk=4)
        self.match_equal_penalty_home_winner = Match.objects.get(pk=5)
        self.match_equal_penalty_away_winner = Match.objects.get(pk=6)
        
        self.match_home_winner.finished = True
        self.match_away_winner.finished = True
        self.match_equal.finished = True
        self.match_equal_0.finished = True
        self.match_equal_penalty_home_winner.finished = True
        self.match_equal_penalty_away_winner.finished = True

        self.match_home_winner.save()
        self.match_away_winner.save()
        self.match_equal.save()
        self.match_equal_0.save()
        self.match_equal_penalty_home_winner.save()
        self.match_equal_penalty_away_winner.save()

    def test_match_summary(self):
        self.assertEqual(self.match_home_winner.summary.royals, 1)
        self.assertEqual(self.match_home_winner.summary.full_houses, 1)
        self.assertEqual(self.match_home_winner.summary.straights, 1)
        self.assertEqual(self.match_home_winner.summary.one_pairs, 2)

        self.assertEqual(self.match_away_winner.summary.royals, 1)
        self.assertEqual(self.match_away_winner.summary.full_houses, 1)
        self.assertEqual(self.match_away_winner.summary.straights, 1)
        self.assertEqual(self.match_away_winner.summary.one_pairs, 2)

        self.assertEqual(self.match_equal.summary.royals, 1)
        self.assertEqual(self.match_equal.summary.full_houses, 2)
        self.assertEqual(self.match_equal.summary.straights, 0)
        self.assertEqual(self.match_equal.summary.one_pairs, 2)

        self.assertEqual(self.match_equal_0.summary.royals, 1)
        self.assertEqual(self.match_equal_0.summary.full_houses, 2)
        self.assertEqual(self.match_equal_0.summary.straights, 0)
        self.assertEqual(self.match_equal_0.summary.one_pairs, 2)

        self.assertEqual(self.match_equal_penalty_home_winner.summary.royals, 3)
        self.assertEqual(self.match_equal_penalty_home_winner.summary.full_houses, 2)
        self.assertEqual(self.match_equal_penalty_home_winner.summary.straights, 0)
        self.assertEqual(self.match_equal_penalty_home_winner.summary.one_pairs, 2)

        self.assertEqual(self.match_equal_penalty_away_winner.summary.royals, 3)
        self.assertEqual(self.match_equal_penalty_away_winner.summary.full_houses, 2)
        self.assertEqual(self.match_equal_penalty_away_winner.summary.straights, 0)
        self.assertEqual(self.match_equal_penalty_away_winner.summary.one_pairs, 2)

    def test_matchset_summary(self):
        self.assertEqual(self.matchset.summary.royals, 10)
        self.assertEqual(self.matchset.summary.full_houses, 10)
        self.assertEqual(self.matchset.summary.straights, 2)
        self.assertEqual(self.matchset.summary.one_pairs, 12)
