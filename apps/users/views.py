from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from users.forms import LoginForm, RegisterForm
from users.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):  # 继承认证类,diy它
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:  # 验证用户名密码 否则返回None
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 表示有这个用户 查处自定义usermodel的用户名,
            if user.check_password(password):  # 表示这个用户密码正确, 这里django存储密码是加密的,必须用其下这个方法加密后比对是否正确
                return user
        except Exception as e:
            return None  # 密码错误返回None


# def user_login(request): # 老的login view
#     if request.method == "POST":
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:  # 用户名密码验证成功
#             login(request, user)  # django执行用户登录
#             return render(request, "index.html")
#         else:
#             return render(request, "login.html", {'msg': "用户名或密码错误"})
#
#     elif request.method == "GET":
#         return render(request, "login.html", {})


class UserView(View):  # 新的login view. 继承了View类,它里面实现get post等方法, 使用类模式写免去了函数模式的判断
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)  # 传递进来的字段先进行表单验证,如果规则通过在进入查库逻辑
        if login_form.is_valid():
            user_name = request.POST.get("username", "")  # 字典取值,如果无,赋值为空
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:  # 用户名密码验证成功
                login(request, user)  # django执行用户登录
                return render(request, "index.html")
            else:
                return render(request, "login.html", {'msg': "用户名或密码错误"})
        else:
            return render(request, "login.html",
                          {'msg': "用户名或密码不符合规则", "login_form": login_form})  # 将django的form验证失败内置信息发给前端展示用


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()  # 实例化register表单
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")  # 字典取值,如果无,赋值为空
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)  # 密码加密存储
            user_profile.is_active = False
            user_profile.save()

            send_register_email(user_name, "register")
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveView(View):#主要功能是修改user_profile里的is_active字段为1
    def get(self, request,active_code):
        all_reocrds = EmailVerifyRecord.objects.filter(code=active_code)
        if all_reocrds:
            for record in all_reocrds:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        return render(request, 'login.html')
