from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from playlist.models import Playlist


class PlaylistsViewTests(APITestCase):

    def setUp(self):
        user = User.objects.create_user(
            username="username",
            password="password",
            first_name="testname"
        )
        self.jwt = str(RefreshToken.for_user(user).access_token)
        Playlist.objects.bulk_create([
            Playlist(name="My playlist1", owner=user),
            Playlist(name="My playlist2", owner=user)
        ])

    def test_response(self):
        """
        response 테스트
        """
        url = reverse('playlists')
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.jwt)
        }
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)