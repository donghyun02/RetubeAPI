from rest_framework import serializers

from playlist.models import Playlist, Song


class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = (
            'id',
            'name',
            'video_id',
            'thumbnail',
            'playlist',
            'created',
        )

class PlaylistSerializer(serializers.ModelSerializer):
    songs = SongSerializer(read_only=True, many=True, allow_null=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'owner', 'songs', 'username', 'created', )
