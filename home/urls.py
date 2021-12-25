from rest_framework import routers, urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home)
]
