from django.test import TestCase

from pishi.models import Team, Match, MatchSet, Predict, User, Score
from pishi.badge import *


class PredictTestCase(TestCase):
    fixtures = ['users.json', 'teams.json', 'matchsets.json', 'matchset_summary.json',
                'matches_r16.json','match_and_predictions.json']

    def setUp(self):
        match_sets = MatchSet.objects.all()
        users = User.objects.all()
        for u in users:
            for ms in match_sets:
                Score.objects.create(match_set=ms, user=u)

        self.match_home_winner = Match.objects.get(pk=1)
        self.p_hw_royal = Predict.objects.get(pk=1)
        self.p_hw_full_house = Predict.objects.get(pk=2)
        self.p_hw_straight = Predict.objects.get(pk=3)
        self.p_hw_one_pair_eq = Predict.objects.get(pk=4)
        self.p_hw_one_pair_aw = Predict.objects.get(pk=5)

        self.match_away_winner = Match.objects.get(pk=2)
        self.p_aw_royal = Predict.objects.get(pk=6)
        self.p_aw_full_house = Predict.objects.get(pk=7)
        self.p_aw_straight = Predict.objects.get(pk=8)
        self.p_aw_one_pair_eq = Predict.objects.get(pk=9)
        self.p_aw_one_pair_hw = Predict.objects.get(pk=10)

        self.match_equal = Match.objects.get(pk=3)
        self.p_eq_royal = Predict.objects.get(pk=11)
        self.p_eq_full_house_0 = Predict.objects.get(pk=12)
        self.p_eq_full_house = Predict.objects.get(pk=13)
        self.p_eq_one_pair_hw = Predict.objects.get(pk=14)
        self.p_eq_one_pair_aw = Predict.objects.get(pk=15)

        self.match_equal_0 = Match.objects.get(pk=4)
        self.p_eq0_royal = Predict.objects.get(pk=16)
        self.p_eq0_full_house = Predict.objects.get(pk=17)
        self.p_eq0_full_house2 = Predict.objects.get(pk=18)
        self.p_eq0_one_pair_hw = Predict.objects.get(pk=19)
        self.p_eq0_one_pair_aw = Predict.objects.get(pk=20)

        self.match_equal_penalty_home_winner = Match.objects.get(pk=5)
        self.p_penalty_hw_royal_royal = Predict.objects.get(pk=21)
        self.p_penalty_hw_royal_straight = Predict.objects.get(pk=22)
        self.p_penalty_hw_royal_onepair = Predict.objects.get(pk=23)
        self.p_penalty_hw_fullhouse_straight = Predict.objects.get(pk=24)
        self.p_penalty_hw_fullhouse_onepair = Predict.objects.get(pk=25)
        self.p_penalty_hw_one_pair_hw = Predict.objects.get(pk=26)
        self.p_penalty_hw_one_pair_aw = Predict.objects.get(pk=27)

        self.match_equal_penalty_away_winner = Match.objects.get(pk=6)
        self.p_penalty_aw_royal_royal = Predict.objects.get(pk=28)
        self.p_penalty_aw_royal_straight = Predict.objects.get(pk=29)
        self.p_penalty_aw_royal_onepair = Predict.objects.get(pk=30)
        self.p_penalty_aw_fullhouse_straight = Predict.objects.get(pk=31)
        self.p_penalty_aw_fullhouse_onepair = Predict.objects.get(pk=32)
        self.p_penalty_aw_one_pair_hw = Predict.objects.get(pk=33)
        self.p_penalty_aw_one_pair_aw = Predict.objects.get(pk=34)

    def test_creation(self):
        with self.assertRaises(Predict.DoesNotExist):
            Predict.objects.get(id=100)
        predict = Predict.objects.create(user_id=1, match_id=53, home_result=1, away_result=2)
        self.assertEqual(predict.winner, predict.match.away_team)
        predict = Predict.objects.create(user_id=2, match_id=53, home_result=3, away_result=2)
        self.assertEqual(predict.winner, predict.match.home_team)
        predict = Predict.objects.create(user_id=3, match_id=53, home_result=2, away_result=2)
        self.assertIsNone(predict.winner)

    def test_winner_in_120(self):
        match = Match.objects.get(pk=1)
        p1 = Predict.objects.create(user_id=10, match=match, home_result=2, away_result=0)
        self.assertEqual(p1.winner, match.home_team)
        p1.delete()
        p1 = Predict.objects.create(user_id=10, match=match, home_result=2, away_result=1)
        self.assertEqual(p1.winner, match.home_team)
        p1.delete()
        p1 = Predict.objects.create(user_id=10, match=match, home_result=1, away_result=2)
        self.assertEqual(p1.winner, match.away_team)
        p1.delete()
        p1 = Predict.objects.create(user_id=10, match=match, home_result=0, away_result=2)
        self.assertEqual(p1.winner, match.away_team)
        p1.delete()
        p1 = Predict.objects.create(user_id=10, match=match, home_result=2, away_result=2)
        self.assertIsNone(p1.winner)
        p1.delete()
        p1 = Predict.objects.create(user_id=10, match=match, home_result=0, away_result=0)
        self.assertIsNone(p1.winner)
        p1.delete()

    def test_winner_in_penalty(self):
        match = Match.objects.get(pk=1)
        p1 = Predict.objects.create(user_id=10, match=match, home_result=2, away_result=1)
        self.assertIsNone(p1.get_winner_in_penalty())
        p1.delete()
        p1 = Predict.objects.create(user_id=10, match=match, home_result=2, away_result=0)
        self.assertIsNone(p1.get_winner_in_penalty())
        p1.delete()
        p1 = Predict.objects.create(user_id=10, match=match, home_result=1, away_result=2)
        self.assertIsNone(p1.get_winner_in_penalty())
        p1.delete()
        p1 = Predict.objects.create(user_id=10, match=match, home_result=0, away_result=2)
        self.assertIsNone(p1.get_winner_in_penalty())
        p1.delete()
        p1 = Predict.objects.create(user_id=10, match=match, home_result=1, away_result=1)
        with self.assertRaises(ValueError):
            p1.get_winner_in_penalty()
        p1.delete()
        p1 = Predict.objects.create(user_id=10, match=match, home_result=1, away_result=1, home_penalty=3,
                                    away_penalty=1)
        self.assertEqual(p1.get_winner_in_penalty(), match.home_team)
        p1.delete()
        p1 = Predict.objects.create(user_id=10, match=match, home_result=1, away_result=1, home_penalty=3,
                                    away_penalty=0)
        self.assertEqual(p1.get_winner_in_penalty(), match.home_team)
        p1.delete()
        p1 = Predict.objects.create(user_id=10, match=match, home_result=1, away_result=1, home_penalty=1,
                                    away_penalty=3)
        self.assertEqual(p1.get_winner_in_penalty(), match.away_team)
        p1.delete()
        p1 = Predict.objects.create(user_id=10, match=match, home_result=1, away_result=1, home_penalty=0,
                                    away_penalty=3)
        self.assertEqual(p1.get_winner_in_penalty(), match.away_team)
        p1.delete()
        p1 = Predict.objects.create(user_id=10, match=match, home_result=0, away_result=0, home_penalty=0,
                                    away_penalty=0)
        with self.assertRaises(ValueError):
            p1.get_winner_in_penalty()
        p1.delete()

    def test_is_royal(self):
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

        self.assertTrue(self.p_hw_royal.is_royal())
        self.assertTrue(self.p_aw_royal.is_royal())
        self.assertTrue(self.p_eq0_royal.is_royal())
        self.assertTrue(self.p_eq_royal.is_royal())
        self.assertTrue(self.p_penalty_hw_royal_royal.is_royal())
        self.assertTrue(self.p_penalty_hw_royal_straight.is_royal())
        self.assertTrue(self.p_penalty_hw_royal_onepair.is_royal())
        self.assertTrue(self.p_penalty_aw_royal_royal.is_royal())
        self.assertTrue(self.p_penalty_aw_royal_straight.is_royal())
        self.assertTrue(self.p_penalty_aw_royal_onepair.is_royal())

    def test_is_fullhouse(self):
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

        self.assertTrue(self.p_hw_full_house.is_full_house())
        self.assertTrue(self.p_aw_full_house.is_full_house())
        self.assertTrue(self.p_eq0_full_house.is_full_house())
        self.assertTrue(self.p_eq0_full_house2.is_full_house())
        self.assertTrue(self.p_eq_full_house.is_full_house())
        self.assertTrue(self.p_eq_full_house_0.is_full_house())
        self.assertTrue(self.p_penalty_hw_fullhouse_straight.is_full_house())
        self.assertTrue(self.p_penalty_hw_fullhouse_onepair.is_full_house())
        self.assertTrue(self.p_penalty_aw_fullhouse_straight.is_full_house())
        self.assertTrue(self.p_penalty_aw_fullhouse_onepair.is_full_house())

    def test_is_straight(self):
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

        self.assertTrue(self.p_hw_straight.is_straight())
        self.assertTrue(self.p_aw_straight.is_straight())
        self.assertFalse(self.p_hw_one_pair_aw.is_straight())
        self.assertFalse(self.p_hw_one_pair_eq.is_straight())
        self.assertFalse(self.p_aw_one_pair_hw.is_straight())
        self.assertFalse(self.p_aw_one_pair_eq.is_straight())
        self.assertFalse(self.p_eq_one_pair_hw.is_straight())
        self.assertFalse(self.p_eq_one_pair_aw.is_straight())
        self.assertFalse(self.p_eq0_one_pair_hw.is_straight())
        self.assertFalse(self.p_eq0_one_pair_aw.is_straight())
        self.assertFalse(self.p_penalty_hw_one_pair_hw.is_straight())
        self.assertFalse(self.p_penalty_hw_one_pair_aw.is_straight())
        self.assertFalse(self.p_penalty_aw_one_pair_hw.is_straight())
        self.assertFalse(self.p_penalty_aw_one_pair_aw.is_straight())

    def test_value_m_hw(self):
        self.assertEqual(self.p_hw_royal.value(), 0)
        self.assertEqual(self.p_hw_full_house.value(), 0)
        self.assertEqual(self.p_hw_straight.value(), 0)
        self.assertEqual(self.p_hw_one_pair_eq.value(), 0)
        self.assertEqual(self.p_hw_one_pair_aw.value(), 0)

        self.match_home_winner.finished = True
        self.match_home_winner.conclude()

        self.p_hw_royal.refresh_from_db()
        self.p_hw_full_house.refresh_from_db()
        self.p_hw_straight.refresh_from_db()
        self.p_hw_one_pair_eq.refresh_from_db()
        self.p_hw_one_pair_aw.refresh_from_db()

        self.assertEqual(self.p_hw_royal.value(), BadgeScore.ROYAL)
        self.assertEqual(self.p_hw_full_house.value(), BadgeScore.FULL_HOUSE)
        self.assertEqual(self.p_hw_straight.value(), BadgeScore.STRAIGHT)
        self.assertEqual(self.p_hw_one_pair_eq.value(), BadgeScore.ONE_PAIR)
        self.assertEqual(self.p_hw_one_pair_aw.value(), BadgeScore.ONE_PAIR)

    def test_value_m_aw(self):
        self.assertEqual(self.p_aw_royal.value(), 0)
        self.assertEqual(self.p_aw_full_house.value(), 0)
        self.assertEqual(self.p_aw_straight.value(), 0)
        self.assertEqual(self.p_aw_one_pair_eq.value(), 0)
        self.assertEqual(self.p_aw_one_pair_hw.value(), 0)

        self.match_away_winner.finished = True
        self.match_away_winner.conclude()

        self.p_aw_royal.refresh_from_db()
        self.p_aw_full_house.refresh_from_db()
        self.p_aw_straight.refresh_from_db()
        self.p_aw_one_pair_eq.refresh_from_db()
        self.p_aw_one_pair_hw.refresh_from_db()

        self.assertEqual(self.p_aw_royal.value(), BadgeScore.ROYAL)
        self.assertEqual(self.p_aw_full_house.value(), BadgeScore.FULL_HOUSE)
        self.assertEqual(self.p_aw_straight.value(), BadgeScore.STRAIGHT)
        self.assertEqual(self.p_aw_one_pair_eq.value(), BadgeScore.ONE_PAIR)
        self.assertEqual(self.p_aw_one_pair_hw.value(), BadgeScore.ONE_PAIR)
        
    def test_value_m_eq(self):
        self.assertEqual(self.p_eq_royal.value(), 0)
        self.assertEqual(self.p_eq_full_house.value(), 0)
        self.assertEqual(self.p_eq_full_house_0.value(), 0)
        self.assertEqual(self.p_eq_one_pair_hw.value(), 0)
        self.assertEqual(self.p_eq_one_pair_aw.value(), 0)

        self.match_equal.finished = True
        self.match_equal.conclude()

        self.p_eq_royal.refresh_from_db()
        self.p_eq_full_house.refresh_from_db()
        self.p_eq_full_house_0.refresh_from_db()
        self.p_eq_one_pair_hw.refresh_from_db()
        self.p_eq_one_pair_aw.refresh_from_db()

        self.assertEqual(self.p_eq_royal.value(), BadgeScore.ROYAL)
        self.assertEqual(self.p_eq_full_house.value(), BadgeScore.FULL_HOUSE)
        self.assertEqual(self.p_eq_full_house_0.value(), BadgeScore.FULL_HOUSE)
        self.assertEqual(self.p_eq_one_pair_hw.value(), BadgeScore.ONE_PAIR)
        self.assertEqual(self.p_eq_one_pair_aw.value(), BadgeScore.ONE_PAIR)
        
    def test_value_m_eq0(self):
        self.assertEqual(self.p_eq0_royal.value(), 0)
        self.assertEqual(self.p_eq0_full_house.value(), 0)
        self.assertEqual(self.p_eq0_full_house2.value(), 0)
        self.assertEqual(self.p_eq0_one_pair_hw.value(), 0)
        self.assertEqual(self.p_eq0_one_pair_aw.value(), 0)

        self.match_equal_0.finished = True
        self.match_equal_0.conclude()

        self.p_eq0_royal.refresh_from_db()
        self.p_eq0_full_house.refresh_from_db()
        self.p_eq0_full_house2.refresh_from_db()
        self.p_eq0_one_pair_hw.refresh_from_db()
        self.p_eq0_one_pair_aw.refresh_from_db()

        self.assertEqual(self.p_eq0_royal.value(), BadgeScore.ROYAL)
        self.assertEqual(self.p_eq0_full_house.value(), BadgeScore.FULL_HOUSE)
        self.assertEqual(self.p_eq0_full_house2.value(), BadgeScore.FULL_HOUSE)
        self.assertEqual(self.p_eq0_one_pair_hw.value(), BadgeScore.ONE_PAIR)
        self.assertEqual(self.p_eq0_one_pair_aw.value(), BadgeScore.ONE_PAIR)

    def test_value_m_penalty_hw(self):
        self.assertEqual(self.p_penalty_hw_royal_royal.value(), 0)
        self.assertEqual(self.p_penalty_hw_royal_straight.value(), 0)
        self.assertEqual(self.p_penalty_hw_royal_onepair.value(), 0)
        self.assertEqual(self.p_penalty_hw_fullhouse_straight.value(), 0)
        self.assertEqual(self.p_penalty_hw_fullhouse_onepair.value(), 0)
        self.assertEqual(self.p_penalty_hw_one_pair_hw.value(), 0)
        self.assertEqual(self.p_penalty_hw_one_pair_aw.value(), 0)

        self.match_equal_penalty_home_winner.finished = True
        self.match_equal_penalty_home_winner.conclude()

        self.p_penalty_hw_royal_royal.refresh_from_db()
        self.p_penalty_hw_royal_straight.refresh_from_db()
        self.p_penalty_hw_royal_onepair.refresh_from_db()
        self.p_penalty_hw_fullhouse_straight.refresh_from_db()
        self.p_penalty_hw_fullhouse_onepair.refresh_from_db()
        self.p_penalty_hw_one_pair_hw.refresh_from_db()
        self.p_penalty_hw_one_pair_aw.refresh_from_db()

        self.assertEqual(self.p_penalty_hw_royal_royal.value(), BadgeScore.ROYAL+BadgeScore.PENALTY)
        self.assertEqual(self.p_penalty_hw_royal_straight.value(), BadgeScore.ROYAL+BadgeScore.PENALTY)
        self.assertEqual(self.p_penalty_hw_royal_onepair.value(), BadgeScore.ROYAL)
        self.assertEqual(self.p_penalty_hw_fullhouse_straight.value(), BadgeScore.FULL_HOUSE+BadgeScore.PENALTY)
        self.assertEqual(self.p_penalty_hw_fullhouse_onepair.value(), BadgeScore.FULL_HOUSE)
        self.assertEqual(self.p_penalty_hw_one_pair_hw.value(), BadgeScore.ONE_PAIR)
        self.assertEqual(self.p_penalty_hw_one_pair_aw.value(), BadgeScore.ONE_PAIR)

    def test_value_m_penalty_aw(self):
        self.assertEqual(self.p_penalty_aw_royal_royal.value(), 0)
        self.assertEqual(self.p_penalty_aw_royal_straight.value(), 0)
        self.assertEqual(self.p_penalty_aw_royal_onepair.value(), 0)
        self.assertEqual(self.p_penalty_aw_fullhouse_straight.value(), 0)
        self.assertEqual(self.p_penalty_aw_fullhouse_onepair.value(), 0)
        self.assertEqual(self.p_penalty_aw_one_pair_hw.value(), 0)
        self.assertEqual(self.p_penalty_aw_one_pair_aw.value(), 0)

        self.match_equal_penalty_away_winner.finished = True
        self.match_equal_penalty_away_winner.conclude()

        self.p_penalty_aw_royal_royal.refresh_from_db()
        self.p_penalty_aw_royal_straight.refresh_from_db()
        self.p_penalty_aw_royal_onepair.refresh_from_db()
        self.p_penalty_aw_fullhouse_straight.refresh_from_db()
        self.p_penalty_aw_fullhouse_onepair.refresh_from_db()
        self.p_penalty_aw_one_pair_hw.refresh_from_db()
        self.p_penalty_aw_one_pair_aw.refresh_from_db()

        self.assertEqual(self.p_penalty_aw_royal_royal.value(), BadgeScore.ROYAL+BadgeScore.PENALTY)
        self.assertEqual(self.p_penalty_aw_royal_straight.value(), BadgeScore.ROYAL+BadgeScore.PENALTY)
        self.assertEqual(self.p_penalty_aw_royal_onepair.value(), BadgeScore.ROYAL)
        self.assertEqual(self.p_penalty_aw_fullhouse_straight.value(), BadgeScore.FULL_HOUSE+BadgeScore.PENALTY)
        self.assertEqual(self.p_penalty_aw_fullhouse_onepair.value(), BadgeScore.FULL_HOUSE)
        self.assertEqual(self.p_penalty_aw_one_pair_hw.value(), BadgeScore.ONE_PAIR)
        self.assertEqual(self.p_penalty_aw_one_pair_aw.value(), BadgeScore.ONE_PAIR)

    def test_predict_winner_after_edit(self):
        match = self.match_home_winner
        predict = self.p_hw_royal
        self.assertEqual(predict.winner, match.home_team)
        predict.home_result = 0
        predict.away_result = 3
        predict.save()
        self.assertEqual(predict.winner, match.away_team)
        predict.home_result = 1
        predict.away_result = 1
        predict.save()
        self.assertIsNone(predict.winner)