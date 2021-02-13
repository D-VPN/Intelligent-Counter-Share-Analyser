from django.urls import path
from . import views
from .views import RetailerRegisterView, BrandRegisterView

urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('retailRegister',views.RetailerRegisterView.as_view(),name='register_retailer'),
    path('brandRegister',views.BrandRegisterView.as_view(),name='register_brand'),
]