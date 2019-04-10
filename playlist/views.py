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
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except:
            status = 404
            message = '존재하지 않는 오브젝트입니다.'
            return Response({'message': message}, status=status)
        else:
            serializer = PlaylistSerializer(playlist)
            message = '요청 성공'
            status = 200
            response = {
                'message': message,
                'data': serializer.data
            }
            return Response(response, status=status)

    def patch(self, request, playlist_id):
        name = request.data.get('name', None)
        if name is None:
            status = 400
            message = '변경할 필드가 포함되어 있지 않은 요청입니다.'
            return Response({'message': message}, status=status)

        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except:
            status = 404
            message = '존재하지 않는 오브젝트입니다.'
            return Response({'message': message}, status=status)
        else:
            playlist.name = name
            playlist.save()

            status = 200
            serializer = PlaylistSerializer(playlist)
            message = '요청 성공'

            response = {
                'message': message,
                'data': serializer.data
            }
            return Response(response, status=status)

    def delete(self, request, playlist_id):
        pass

