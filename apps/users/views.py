from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from users.models import UserProfile


class CustomBackend(ModelBackend):  # 继承认证类,diy它
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:  # 验证用户名密码 否则返回None
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 表示有这个用户 查处自定义usermodel的用户名,
            if user.check_password(password):  # 表示这个用户密码正确, 这里django存储密码是加密的,必须用其下这个方法加密后比对是否正确
                return user
        except Exception as e:
            return None  # 密码错误返回None


def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:  # 用户名密码验证成功
            login(request, user)  # django执行用户登录
            return render(request, "index.html")
        else:
            return render(request, "login.html", {'msg':"用户名或密码错误"})

    elif request.method == "GET":
        return render(request, "login.html", {})
