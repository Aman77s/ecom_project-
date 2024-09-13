
from django.urls import path
from . import views 


urlpatterns = [
    path('', views.home , name='home'),
    path('about/', views.about, name='about' ),
    path('signin/', views.signin_user, name='signin'),
    path('signout/', views.signout_user, name='signout'),
    path('signup/', views.signup_user, name='signup'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('category_summery/', views.category_summery, name='category_summery'),
    path('user_update', views.user_update, name='user_update'),
    path('update_info/', views.update_info, name='update_info'),
    path('search/', views.search, name='search'),
    path('new/', views.new, name="new")
] 