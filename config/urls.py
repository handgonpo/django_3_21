from django.contrib import admin
from django.urls import path, include #include 포함시킨다는 의미

urlpatterns = [
    path("admin/", admin.site.urls), 
    path("", include("users.urls")) #users.urls로 이동
]
