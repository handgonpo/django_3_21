from django.urls import path
from . import views  # .의 뜻은 현재 위치를 뜻하며 from users import views란 뜻

urlpatterns = [
    path("", views.index, name='index'),
    path("read/<id>/", views.read,name='read'),
    path("create/", views.create, name='create'),
    path("delete/", views.delete, name='delete'),
]
