from django.urls import path
from . import views  # .의 뜻은 현재 위치를 뜻하며 from users import views란 뜻

urlpatterns = [
    path("", views.index),
    path("read/<id>/", views.read),
    path("create/", views.create),
    path("delete/", views.delete)
]
