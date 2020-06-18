"""plasmabank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from plasmadonor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('singin', views.singin, name='singin'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name="logout"),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('delete_account/<int:id>',views.delete_account, name='delete_account'),
    path('password_reset/', views.PasswordReset.as_view(),name ='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(),name ='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(),name ='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(),name ='password_reset_complete'),
    path('story',views.Story, name='story'),
    path('storyadd', views.storyadd, name='sorryadd'),
]
