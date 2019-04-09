from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from playlist.models import Playlist


class PlaylistsViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="username",
            password="password",
            first_name="testname"
        )
        self.jwt = str(RefreshToken.for_user(self.user).access_token)
        self.url = reverse('playlists')
        self.headers = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.jwt)
        }

    def test_get_response(self):
        """
        GET response 테스트
        """
        Playlist.objects.bulk_create([
            Playlist(name="My playlist1", owner=self.user),
            Playlist(name="My playlist2", owner=self.user)
        ])
        response = self.client.get(self.url, **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_post_no_name_response(self):
        """
        POST response 에서 파라미터에 name 필드가 없을 경우
        """
        response = self.client.post(self.url, **self.headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get('message', None), 'name 필드는 필수 필드입니다.')

    def test_post_success_response(self):
        """
        POST response 성공시
        """
        data = {
            'name': 'TestPlaylist'
        }
        response = self.client.post(self.url, data=data, **self.headers)
        playlist = Playlist.objects.filter(user=self.user, name="TestPlaylist")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(playlist.exists())


