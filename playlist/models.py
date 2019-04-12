from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Playlist(models.Model):
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(User, related_name="playlists", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.owner.first_name, self.name)


class Song(models.Model):
    name = models.CharField(max_length=256)
    video_id = models.CharField(max_length=32)
    thumbnail = models.TextField()
    order = models.PositiveIntegerField(default=0)
    playlist = models.ForeignKey(
        Playlist,
        related_name="songs",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('order', )