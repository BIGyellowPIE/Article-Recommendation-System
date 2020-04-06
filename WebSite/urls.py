from django.contrib import admin
from django.urls import path
from django.urls import include
from login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('captcha/', include('captcha.urls')),   # 增加这一行
    path('prefer/', views.prefer),
    path('search/', include('haystack.urls')),
    path('channel/', views.channel),
    path('record/', views.record),
    path('faqs/', views.faqs),
    path('help/', views.help),
]
