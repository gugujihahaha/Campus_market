"""
URL configuration for campus_market project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/goods/", permanent=False), name="home"),
    # 便捷短链接：不带 /goods/ 前缀也能访问
    path("register/", RedirectView.as_view(url="/goods/register/", permanent=False)),
    path("login/", RedirectView.as_view(url="/goods/login/", permanent=False)),
    path("logout/", RedirectView.as_view(url="/goods/logout/", permanent=False)),
    path("add/", RedirectView.as_view(url="/goods/add/", permanent=False)),
    path('goods/', include('goods.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
