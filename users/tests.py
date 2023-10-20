from django.test import TestCase
from .models import User
# Create your tests here.


class UserModelTest(TestCase):

    def setUpTestData():
        User.objects.create(name='George')

    def test_user_name(self):
        user = User.objects.get(id=1)
        user_label = user._meta.get_field('name').verbose_name
        self.assertEqual(user_label, 'name')

    def test_user_name_length(self):
        user = User.objects.get(id=1)
        user_max_length = user._meta.get_field('name').max_length
        self.assertEqual(user_max_length, 50)
