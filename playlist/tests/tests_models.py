from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase

# Create your tests here.
from playlist.models import Playlist, Song


class PlaylistTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='username',
            password='password',
            first_name='testname'
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
        self.assertTrue(field.auto_now_add)

    def test_str(self):
        """
        __str__ 매직메서드 테스트
        """
        title = str(self.playlist)
        owner_first_name = self.playlist.owner.first_name
        name = self.playlist.name
        self.assertEqual(title, '{} - {}'.format(owner_first_name, name))

class SongTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(
            username="username",
            password="password",
            first_name="testname"
        )
        playlist = Playlist.objects.create(
            name="My play list",
            owner=user
        )
        self.song = Song.objects.create(
            name="Song",
            video_id="test_video_id",
            thumbnail="https://thumbnail.url",
        )
        self.song.playlists.add(playlist)

    def test_verbose_name(self):
        """
        모델 이름 테스트
        """
        verbose_name = self.song._meta.verbose_name
        self.assertEqual(verbose_name, 'song')

    def test_name_field(self):
        """
        name 필드 테스트
        """
        field = self.song._meta.get_field('name')
        self.assertTrue(field, models.CharField)
        self.assertEqual(field.verbose_name, 'name')
        self.assertEqual(field.max_length, 256)

    def test_video_id_field(self):
        """
        video_id 필드 테스트
        """
        field = self.song._meta.get_field('video_id')
        self.assertTrue(field, models.CharField)
        self.assertEqual(field.verbose_name, 'video id')
        self.assertEqual(field.max_length, 32)
        self.assertTrue(field._unique)

    def test_thumbnail_field(self):
        """
        thumbnail 필드 테스트
        """
        field = self.song._meta.get_field('thumbnail')
        self.assertTrue(field, models.TextField)
        self.assertEqual(field.verbose_name, 'thumbnail')

    def test_playlists_field(self):
        """
        playlists 필드 테스트
        """
        field = self.song._meta.get_field('playlists')
        self.assertTrue(field, models.ManyToManyField)
        self.assertEqual(field.verbose_name, 'playlists')
        self.assertEqual(field.related_model, Playlist)

    def test_created_field(self):
        """
        created 필드 테스트
        """
        field = self.song._meta.get_field('created')
        self.assertTrue(field, models.DateTimeField)
        self.assertEqual(field.verbose_name, 'created')
        self.assertTrue(field.auto_now_add)

    def test_str_(self):
        """
        __str__ 매직 메서드 테스트
        """
        self.assertEqual(str(self.song), self.song.name)

    def test_indexed_fields(self):
        """
        인덱싱 필드 테스트
        """
        video_id_index = models.Index(fields=['video_id']).fields
        indexes = (index.fields for index in self.song._meta.indexes)
        self.assertTrue(video_id_index in indexes)