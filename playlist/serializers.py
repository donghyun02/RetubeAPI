from rest_framework import serializers

from accounts.serializers import UserSerializer
from playlist.models import Playlist, Song


class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = ('id', 'name', 'video_id', 'thumbnail', 'playlist', 'created')

class PlaylistSerializer(serializers.ModelSerializer):
    songs = SongSerializer(read_only=True, many=True)

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'owner__username', 'song', 'created', )
