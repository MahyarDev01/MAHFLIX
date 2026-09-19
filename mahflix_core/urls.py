"""
URL configuration for mahflix_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path, include
from pages import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),

    path('wallet/', views.wallet_view, name='wallet'),
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.search_view, name='search'),
    path('movies/', views.movies_view, name='movies'),
    path('comments/', views.comments_view, name='comments'),

    path('register/', views.register_view, name='register'),
    path('otp-verify/', views.otp_verify_view, name='otp_verify'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('new-password/', views.new_password_view, name='new_password'),

    path('api/users/', include('users.urls')),
    path('api/content/', include('content.urls')),
    path('api/finance/', include('finance.urls')),
]

