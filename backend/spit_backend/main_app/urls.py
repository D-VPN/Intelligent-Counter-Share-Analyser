from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('retailRegister',views.login,name='register_retailer'),
    path('brandRegister',views.login,name='register_brand'),
]