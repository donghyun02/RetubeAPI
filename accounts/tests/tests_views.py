from django.contrib.auth.models import User
from django.test import TestCase
# Create your tests here.
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterViewTests(TestCase):

    def test_no_data(self):
        """
        아이디, 비밀번호, 이름이 전송되지 않았을 경우
        """
        data = {}

        response = self.client.post(
            reverse('register'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('message', None),
            '아이디를 입력해주세요.'
        )

    def test_no_username(self):
        """
        아이디가 전송되지 않았을 경우
        """
        data = {
            'password': 'password',
            'name': 'name'
        }

        response = self.client.post(
            reverse('register'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('message', None),
            '아이디를 입력해주세요.'
        )

    def test_no_password(self):
        """
        비밀번호가 전송되지 않았을 경우
        """
        data = {
            'username': 'username',
            'name': 'name'
        }

        response = self.client.post(
            reverse('register'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('message', None),
            '비밀번호를 입력해주세요.'
        )

    def test_no_name(self):
        """
        이름이 전송되지 않았을 경우
        """
        data = {
            'username': 'username',
            'password': 'password',
        }

        response = self.client.post(
            reverse('register'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('message', None),
            '이름을 입력해주세요.'
        )

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

        User.objects.create_user(
            username=username,
            password=password,
            first_name=name
        )
        response = self.client.post(
            reverse('register'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('message', None),
            '이미 존재하는 아이디입니다.'
        )

    def test_register_success(self):
        """
        회원가입에 성공한 경우
        """
        data = {
            'username': 'username',
            'password': 'pass',
            'name': 'name'
        }

        response = self.client.post(
            reverse('register'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data.get('message', None),
            '회원가입이 완료되었습니다.'
        )


class LoginViewTests(TestCase):

    def test_no_username(self):
        """
        존재하지 않는 아이디일 경우
        """
        data = {
            'username': 'username',
            'password': 'password'
        }

        response = self.client.post(
            reverse('login'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('message', None),
            '존재하지 않는 아이디입니다.'
        )

    def test_wrong_password(self):
        """
        비밀번호가 맞지 않을 경우
        """
        username = 'username'
        password = 'password'
        wrong_password = 'wrongpassword'
        data = {
            'username': username,
            'password': wrong_password
        }

        User.objects.create_user(username=username, password=password)
        response = self.client.post(
            reverse('login'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('message', None),
            '잘못된 비밀번호입니다.'
        )

    def test_login_success(self):
        """
        로그인에 성공할 경우
        """
        username = 'username'
        password = 'password'
        data = {
            'username': username,
            'password': password
        }

        User.objects.create_user(username=username, password=password)
        response = self.client.post(
            reverse('login'),
            data=data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data.get('message', None),
            '로그인에 성공하였습니다.'
        )


def create_access_jwt(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


class UserInfoViewTests(TestCase):

    def test_no_jwt(self):
        """
        JWT 가 헤더에 포함되어 있지 않은 경우
        """
        response = self.client.get(reverse('user-info'))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data.get('detail', None),
            'Authentication credentials were not provided.'
        )

    def test_jwt_invalid_or_expired(self):
        """
        JWT 가 만료되거나 잘못된 경우
        """
        jwt = 'somethingwrongjwt'
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(jwt)
        }
        response = self.client.get(reverse('user-info'), **headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data.get('detail', None),
            'Given token not valid for any token type'
        )

    def test_success(self):
        """
        요청에 성공한 경우
        """
        username = 'username'
        password = 'password'
        name = 'name'
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=name
        )
        jwt = create_access_jwt(user)
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(jwt)
        }

        response = self.client.get(reverse('user-info'), **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data.get('message', None),
            '확인된 사용자입니다.'
        )
        self.assertEqual(response.data.get('name', None), 'name')