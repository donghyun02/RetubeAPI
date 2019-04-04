from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class RegisterViewTests(TestCase):
    def test_no_data(self):
        """
        아이디, 비밀번호, 이름이 전송되지 않았을 경우
        """
        data = {}
        response = self.client.post(reverse('register'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('message', None), '아이디를 입력해주세요.')

    def test_no_username(self):
        """
        아이디가 전송되지 않았을 경우
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
        비밀번호가 전송되지 않았을 경우
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
        이름이 전송되지 않았을 경우
        """
        data = {
            'username': 'username',
            'password': 'password',
        }
        response = self.client.post(reverse('register'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('message', None), '이름을 입력해주세요.')

    def test_already_exist(self):
        """
        계정이 이미 존재할 경우
        """
        username = 'testusername'
        password = 'testapssword'
        name = 'testuser'
        data = {
            'username': username,
            'password': password,
            'name': name
        }

        User.objects.create_user(username=username, password=password, first_name=name)
        response = self.client.post(reverse('register'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('message', None), '이미 존재하는 아이디입니다.')

    def test_register_success(self):
        """
        회원가입에 성공한 경우
        """
        data = {
            'username': 'username',
            'password': 'pass',
            'name': 'name'
        }
        response = self.client.post(reverse('register'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message', None), '회원가입이 완료되었습니다.')