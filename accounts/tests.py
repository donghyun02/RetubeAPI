from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class RegisterViewTests(TestCase):
    def test_no_data(self):
        """
        아이디, 비밀번호, 이름이 전송되지 않았을 때
        """
        data = {}
        response = self.client.post(reverse('register'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('message', None), '아이디를 입력해주세요.')

    def test_no_username(self):
        """
        아이디가 전송되지 않았을 때
        """
        data = {
            'password': 'password',
            'name': 'name'
        }
        response = self.client.post(reverse('register'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('message', None), '아이디를 입력해주세요.')

    def test_no_password(self):
        """
        비밀번호가 전송되지 않았을 때
        """
        data = {
            'username': 'username',
            'name': 'name'
        }
        response = self.client.post(reverse('register'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('message', None), '비밀번호를 입력해주세요.')

    def test_no_name(self):
        """
        이름이 전송되지 않았을 때
        """
        data = {
            'username': 'username',
            'password': 'password',
        }
        response = self.client.post(reverse('register'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('message', None), '이름을 입력해주세요.')