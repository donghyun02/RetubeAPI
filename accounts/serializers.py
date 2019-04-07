from django.contrib.auth.models import User
from rest_framework import serializers

from playlist.serializers import PlaylistSerializer


class UserSerializer(serializers.ModelSerializer):
    playlists = PlaylistSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'playlists', )
