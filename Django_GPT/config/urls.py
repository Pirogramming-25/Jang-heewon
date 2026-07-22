"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import include, path
from django.shortcuts import redirect
from my_gpt import views

urlpatterns = [
    path("", lambda request: redirect("sentiment/")),
    path("admin/", admin.site.urls),
    
    # Django 기본 accounts URL보다 '위에' 위치해야 커스텀 logout_view가 우선 적용됩니다!
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/signup/', views.signup_view, name='signup'),
    
    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),
    path("", include("my_gpt.urls")),
]