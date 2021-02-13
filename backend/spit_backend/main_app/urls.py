from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import RetailerRegisterView, BrandRegisterView, RetailerListView

urlpatterns = [
    path('',views.index,name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register', views.register, name='register'),
    path('retailerInfo', views.retailer_info, name='retailer_info'),
    path('contract/<int:id>', views.contract_view, name='contract'),
    path('retailRegister',views.RetailerRegisterView.as_view(),name='register_retailer'),
    path('brandRegister', views.BrandRegisterView.as_view(), name='register_brand'),
    path('brandContract',views.RetailerListView.as_view(),name='brand_contract'),
    path('camera/',views.camera_on,name='camera'),
    path('verify/',views.verify,name='verify'),

]

