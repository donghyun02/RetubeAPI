from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from playlist.models import Playlist


class PlaylistsViewTests(TestCase):

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
        self.assertEqual(len(response.data.get('data', None)), 2)
        self.assertEqual(response.data.get('message', None), '요청 성공')

    def test_post_no_name_response(self):
        """
        POST response 에서 파라미터에 name 필드가 없을 경우
        """
        response = self.client.post(
            self.url,
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('message', None),
            'name 필드는 필수 필드입니다.'
        )

    def test_post_success_response(self):
        """
        POST response 성공시
        """
        name = 'TestPlaylist'
        data = {
            'name': name
        }
        response = self.client.post(
            self.url,
            data=data,
            content_type='application/json',
            **self.headers
        )
        print(response.status_code)
        print(response.data)
        playlist = Playlist.objects.filter(owner=self.user, name=name)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(playlist.exists())
        self.assertEqual(response.data.get('message', None), '요청 성공')


class PlaylistViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testusername",
            password="testpassword",
            first_name="testname"
        )
        self.jwt = str(RefreshToken.for_user(self.user).access_token)
        self.headers = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(self.jwt)
        }

    def test_get_no_object_response(self):
        """
        GET 메서드 요청에서 찾고자 하는 id의 오브젝트가 없을 경우
        """
        url = resolve_url('playlist', playlist_id=1)
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data.get('message', None),
            '존재하지 않는 오브젝트입니다.'
        )

    def test_get_success_response(self):
        """
        GET 메서드 요청에 성공했을 경우
        """
        playlist = Playlist.objects.create(name="test play list", owner=self.user)
        url = resolve_url('playlist', playlist_id=playlist.id)
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data.get('message', None),
            '요청 성공'
        )


    def test_patch_no_object_response(self):
        """
        PATCH 메서드 요청에서 오브젝트가 존재하지 않을 경우
        """
        data = {
            'name': 'Test Name'
        }
        url = resolve_url('playlist', playlist_id=1)
        response = self.client.patch(
            url,
            data=data,
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data.get('message', None),
            '존재하지 않는 오브젝트입니다.'
        )

    def test_patch_no_data_response(self):
        """
        PATCH 메서드 요청에서 데이터가 존재하지 않을 경우
        """
        playlist = Playlist.objects.create(name="New Playlist", owner=self.user)
        url = resolve_url('playlist', playlist_id=playlist.id)
        response = self.client.patch(url, **self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('message', None),
            '변경할 필드가 포함되어 있지 않은 요청입니다.'
        )

    def test_patch_success_response(self):
        """
        PATCH 메서드 요청에 성공했을 때
        """
        playlist = Playlist.objects.create(
            name="Created Playlist",
            owner=self.user
        )
        name = 'Changed Playlist'
        data = {
            'name': name
        }
        url = resolve_url('playlist', playlist_id=playlist.id)
        response = self.client.patch(
            url,
            data=data,
            content_type='application/json',
            **self.headers
        )
        playlist.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message', None), '요청 성공')
        self.assertEqual(playlist.name, name)

    def test_patch_over_length_of_name_field(self):
        """
        PATCH 메서드 요청에서 name 필드의 max_length를 넘는 요청이 올 경우
        """
        playlist = Playlist.objects.create(name="Test", owner=self.user)
        data = {
            'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        }
        url = resolve_url('playlist', playlist_id=playlist.id)
        response = self.client.patch(
            url,
            data=data,
            content_type='application/json',
            **self.headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('message', None), '잘못된 요청입니다.')