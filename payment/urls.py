from django.urls import path
from . import views 


urlpatterns = [
    path('', views.payment_sucess , name='payment_sucess'),
    path('checkout/', views.checkout, name='checkout'),
] 