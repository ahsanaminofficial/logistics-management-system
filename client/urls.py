from rest_framework import routers, urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('products', views.products_info),
    path('home_view', views.clients),
    path('seller', views.client_seller_info),
    path('track', views.client_track_pack),
    path('track/prod', views.client_prod_details),
    path('track/rider', views.client_rider_info),
    path('track/location', views.client_currentloc),
    path('', views.client_home)
]
