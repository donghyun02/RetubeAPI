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

        user = User.objects.create_user(
            username=self.username,
            password=self.password,
            first_name=self.name
        )
        self.playlist = Playlist.objects.create(name="My playlist", owner=user)

    def test_name(self):
        """
        모델의 이름이 제대로 작성되었는지 테스트
        """
        verbose_name = self.playlist._meta.verbose_name
        self.assertEqual(verbose_name, 'playlist')

    def test_name_field(self):
        """
        name 필드가 제대로 작성되었는지 테스트
        """
        field = self.playlist._meta.get_field('name')
        self.assertTrue(isinstance(field, models.CharField))
        self.assertEqual(field.verbose_name, 'name')
        self.assertEqual(field.max_length, 32)

    def test_owner_field(self):
        """
        owner 필드가 제대로 작성되었는지 테스트
        """
        field = self.playlist._meta.get_field('owner')
        self.assertTrue(isinstance(field, models.ForeignKey))
        self.assertEqual(field.verbose_name, 'owner')
        self.assertEqual(field.related_model, User)

    def test_created_field(self):
        """
        created 필드가 제대로 작성되었는지 테스트
        """
        field = self.playlist._meta.get_field('created')
        self.assertTrue(isinstance(field, models.DateTimeField))
        self.assertEqual(field.verbose_name, 'created')
        self.assertEqual(field.auto_now_add, True)

    def test_str(self):
        """
        __str__ 매직메서드 테스트
        """
        title = str(self.playlist)
        owner_first_name = self.playlist.owner.first_name
        name = self.playlist.name
        self.assertEqual(title, '{} - {}'.format(owner_first_name, name))

