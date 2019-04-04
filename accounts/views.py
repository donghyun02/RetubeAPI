from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class RegisterView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        name = request.data.get('name', None)

        if username is None:
            status = 400
            message = '아이디를 입력해주세요.'
            return Response({'message': message}, status=status)

        elif password is None:
            status = 400
            message = '비밀번호를 입력해주세요.'
            return Response({'message': message}, status=status)

        elif name is None:
            status = 400
            message = '이름을 입력해주세요.'
            return Response({'message': message}, status=status)

        user = User.objects.filter(username=username)
        if user.exists():
            status = 400
            message = '이미 존재하는 아이디입니다.'
            return Response({'message': message}, status=status)

        User.objects.create_user(username=username, password=password, first_name=name)
        status = 201
        message = '회원가입이 완료되었습니다.'
        return Response({'message': message}, status=status)

# class LoginView(APIView):
#     def get(self, request):
#         pass

