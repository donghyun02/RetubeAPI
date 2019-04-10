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
            # request에 name 필드가 없을 경우
            status = 400
            message = 'name 필드는 필수 필드입니다.'
            return Response({'message': message}, status=status)

        # name 필드가 있을 경우
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
            # 요청 받은 id를 가진 오브젝트가 있는 지 검사
            playlist = Playlist.objects.get(id=playlist_id)

        except:
            # 오브젝트가 없을 경우
            status = 404
            message = '존재하지 않는 오브젝트입니다.'
            return Response({'message': message}, status=status)

        else:
            # 오브젝트가 있을 경우
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
            # name 필드가 없을 경우
            status = 400
            message = '변경할 필드가 포함되어 있지 않은 요청입니다.'
            return Response({'message': message}, status=status)

        try:
            # name 필드가 있을 경우 업데이트할 오브젝트가 존재하는 지 검사
            playlist = Playlist.objects.get(id=playlist_id)

        except:
            # 오브젝트가 존재하지 않을 경우
            status = 404
            message = '존재하지 않는 오브젝트입니다.'
            return Response({'message': message}, status=status)

        else:
            # 오브젝트가 존재할 경우 업데이트
            serializer = PlaylistSerializer(
                playlist,
                data={'name': name},
                partial=True
            )

            if serializer.is_valid():
                serializer.save()

                status = 200
                message = '요청 성공'
                response = {
                    'message': message,
                    'data': serializer.data
                }
                return Response(response, status=status)

            else:
                status = 400
                message = '잘못된 요청입니다.'
                return Response({'message': message}, status=status)

    def delete(self, request, playlist_id):
        try:
            # 오브젝트가 있는 지 검사
            playlist = Playlist.objects.get(id=playlist_id)

        except:
            # 오브젝트가 없을 경우 404 리턴
            status = 404
            message = '존재하지 않는 오브젝트입니다.'
            return Response({'message': message}, status=status)

        else:
            # 오브젝트가 있을 경우 삭제
            playlist.delete()
            serializer = PlaylistSerializer(playlist)
            status = 200
            message = '요청 성공'
            response = {
                'message': message,
                'data': serializer.data
            }
            return Response(response, status=status)