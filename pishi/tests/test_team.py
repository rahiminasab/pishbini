from django.test import TestCase
from pishi.models import Team


class TeamTestCase(TestCase):
    def setUp(self):
        Team.objects.create(name='Iran', rank=19,
                            fifa_code='IRA', iso2='IR',
                            flag='https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Flag_of_Iran.svg/630px-Flag_of_Iran.png')

    def test_team_creation(self):
        iran = Team.objects.get(name="Iran")
        self.assertEqual(iran.rank, 19)
        self.assertEqual(iran.fifa_code, 'IRA')
        self.assertEqual(iran.iso2, 'IR')
        self.assertEqual(iran.flag, 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Flag_of_Iran.svg/630px-Flag_of_Iran.png')
        self.assertIsNone(iran.emoji)
        self.assertIsNone(iran.emoji_string)
