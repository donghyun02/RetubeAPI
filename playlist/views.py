from django.db.models import F
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from playlist.models import Playlist
from playlist.serializers import PlaylistSerializer


class PlaylistsView(APIView):

    def get(self, request):
        playlists = Playlist.objects\
            .filter(owner=request.user)\
            .annotate(username=F('owner__first_name'))\
            .order_by('created')
        serializer = PlaylistSerializer(playlists, many=True)
        status = 200
        return Response(serializer.data, status=status)