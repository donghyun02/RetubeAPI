from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class RegisterViewTests(TestCase):
    def test_no_username(self):
        """
        유저이름이 전송되지 않았을 때
        """
        data = {
            'password': 'password',
            'name': 'name'
        }
        response = self.client.post(reverse('register'), data=data, content_type='application/json')
        print(response)