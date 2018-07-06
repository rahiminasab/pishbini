from django.test import TestCase
from pishi.models import Team


class TeamTestCase(TestCase):
    fixtures = ['teams.json']
    
    def setUp(self):
        pass

    def test_team_creation(self):
        with self.assertRaises(Team.DoesNotExist):
            unknown = Team.objects.get(name='unknown')
        unknown = Team.objects.create(name='Unknown', rank=1,
                            fifa_code='UNK', iso2='UN',
                            flag='https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Flag_of_Unknown.svg/630px-Flag_of_Unknown.png')
        self.assertEqual(unknown.rank, 1)
        self.assertEqual(unknown.fifa_code, 'UNK')
        self.assertEqual(unknown.iso2, 'UN')
        self.assertEqual(unknown.flag, 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Flag_of_Unknown.svg/630px-Flag_of_Unknown.png')
        self.assertIsNone(unknown.emoji)
        self.assertIsNone(unknown.emoji_string)

    def test_team_fields(self):
        iran = Team.objects.get(name='Iran')
        self.assertEqual(iran.rank, 37)
        self.assertEqual(iran.fifa_code, 'IRN')
        self.assertEqual(iran.iso2, u'ir')
