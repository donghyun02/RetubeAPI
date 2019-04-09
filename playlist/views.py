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
        response = {
            'message': '요청 성공',
            'data': serializer.data
        }
        status = 200
        return Response(response, status=status)

    def post(self, request):
        name = request.data.get('name', None)

        if name is None:
            status = 400
            message = 'name 필드는 필수 필드입니다.'
            return Response({'message': message}, status=status)

        playlist = Playlist.objects.create(name=name, owner=request.user)
        serializer = PlaylistSerializer(playlist)
        response = {
            'message': '요청 성공',
            'data': serializer.data
        }
        status = 201
        return Response(response, status=status)


class PlaylistView(APIView):

    def get(self, request, playlist_id):
        pass

    def put(self, request, playlist_id):
        pass

    def patch(self, request, playlist_id):
        pass

    def delete(self, request, playlist_id):
        pass

