from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase

# Create your tests here.
from playlist.models import Playlist


class PlaylistTests(TestCase):

    def setUp(self):
        self.username = "username"
        self.password = "password"
        self.name = "testname"

        user = User.objects.create_user(username=self.username, password=self.password, first_name=self.name)
        Playlist.objects.create(name="My playlist", owner=user)
        Playlist.objects.create(name="My playlist2", owner=user)

    def test_model_creation(self):
        """
        Playlist 모델 생성 테스트
        """
        playlist = Playlist.objects.get(name="My playlist")
        self.assertTrue(isinstance(playlist, Playlist))
        self.assertEqual(playlist.__str__(), 'testname - My playlist')

    # def test_reverse_relationship(self):
    #     """
    #     User 모델과의 역참조 관계 테스트
    #     """
    #     user = User.objects.get(username=self.username)
