"""mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
import xadmin
from mxonline.settings import MEDIA_ROOT
from users import views
from organization import views as org_views
from django.views.static import serve
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name="index"),
    path('login/', views.UserView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('active/<str:active_code>/', views.ActiveView.as_view(), name="active"),
    path('forget_pwd/', views.ForgetPwdView.as_view(), name="forget_pwd"),
    path('reset_pwd/<str:active_code>/', views.ResetPwdView.as_view(), name="reset_pwd"),
    path('modify_pwd/', views.ModifyPwdView.as_view(), name="modify_pwd"),
    # url(r'^active/(?P<active_code>.*)/$', views.ActiveView.as_view(), name="active"),
    path('xadmin/', xadmin.site.urls),
    path('captcha/', include('captcha.urls')),

    # 课程机构
    path('org_list/', org_views.OrgView.as_view(), name="org_list"),
    ## 配置上传文件的访问处理函数
    # path('media/<slug:path>/', serve, {'document_root':MEDIA_ROOT}),
    url(r'^media/(?P<path>.*)', serve, {'document_root':MEDIA_ROOT}),
]
