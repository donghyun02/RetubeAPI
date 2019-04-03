from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class RegisterView(View):
    def post(self, request):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        name = request.POST.get('name', None)

        if username is None:
            status = 400
            message = '아이디를 입력해주세요.'
            return JsonResponse({'message': message}, status=status)

        elif password is None:
            status = 400
            message = '비밀번호를 입력해주세요.'
            return JsonResponse({'message': message}, status=status)

        elif name is None:
            status = 400
            message = '이름을 입력해주세요.'
            return JsonResponse({'message': message}, status=status)

        user = User.objects.filter(username=username)
        if user.exists():
            status = 400
            message = '이미 존재하는 아이디입니다.'
            return JsonResponse({'message': message}, status=status)

        User.objects.create_user(username=username, password=password, first_name=name)
        status = 200
        message = '회원가입이 완료되었습니다.'
        return JsonResponse({'message': message}, status=status)
