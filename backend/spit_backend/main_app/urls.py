from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import RetailerRegisterView, BrandRegisterView

urlpatterns = [
    path('',views.index,name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('retailRegister',views.RetailerRegisterView.as_view(),name='register_retailer'),
    path('brandRegister',views.BrandRegisterView.as_view(),name='register_brand'),
]