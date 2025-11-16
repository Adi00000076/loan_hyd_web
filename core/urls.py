from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('emi-calculator/', views.emi_calculator, name='emi_calculator'),
    path('emi-pdf/', views.emi_pdf, name='emi_pdf'),
]
