from django.contrib.auth import authenticate
from django.contrib.auth.models import User
# Create your views here.
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        name = request.data.get('name', None)

        # 아이디가 안 보내졌을 경우
        if username is None:
            status = 400
            message = '아이디를 입력해주세요.'
            return Response({'message': message}, status=status)

        # 비밀번호가 안 보내졌을 경우
        elif password is None:
            status = 400
            message = '비밀번호를 입력해주세요.'
            return Response({'message': message}, status=status)

        # 사용자 이름이 안 보내졌을 경우
        elif name is None:
            status = 400
            message = '이름을 입력해주세요.'
            return Response({'message': message}, status=status)

        # 아이디가 이미 존재하는지 검사
        try:
            User.objects.get(username=username)

        # 아이디가 없을 경우 회원가입
        except User.DoesNotExist:
            User.objects.create_user(
                username=username,
                password=password,
                first_name=name
            )
            status = 201
            message = '회원가입이 완료되었습니다.'
            return Response({'message': message}, status=status)

        # 아이디가 존재할 경우
        else:
            status = 400
            message = '이미 존재하는 아이디입니다.'
            return Response({'message': message}, status=status)


class LoginView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        # 유저가 존재하는지 검사
        try:
            User.objects.get(username=username)

        # 유저가 존재하지 않을 경우
        except User.DoesNotExist:
            status = 400
            message = '존재하지 않는 아이디입니다.'
            return Response({'message': message}, status=status)

        # 유저가 존재할 경우
        else:
            user = authenticate(username=username, password=password)

            # 비밀번호가 잘못된 경우
            if user is None:
                status = 400
                message = '잘못된 비밀번호입니다.'
                return Response({'message': message}, status=status)

            # 로그인에 성공했을 경우
            else:
                jwt = self.create_jwt(user)
                status = 200
                message = '로그인에 성공하였습니다.'
                return Response(
                    {'message': message, 'jwt': jwt},
                    status=status
                )


    def create_jwt(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class UserInfoView(APIView):

    def get(self, request):
        status = 200
        message = '확인된 사용자입니다.'
        name = request.user.first_name
        return Response({'message': message, 'name': name}, status=status)
