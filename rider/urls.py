from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('home', views.home),
    path('client_info', views.get_client_information),
    path('seller_info', views.get_seller_information),
    path('prod_det', views.get_product_details),
    path('finances', views.get_finances)
]
