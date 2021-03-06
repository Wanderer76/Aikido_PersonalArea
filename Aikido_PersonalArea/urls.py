"""Aikido_PersonalArea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/clubs/', include('clubs.urls')),
    path('api/v1/events/', include('events.urls')),
    path('api/v1/account/', include('PersonalArea.urls')),
]

urlpatterns += static(settings.POSTER_URL, document_root=settings.POSTER_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.COMPONENT_TRAINER_URL, document_root=settings.COMPONENT_TRAINER)
urlpatterns += static(settings.COMPONENT_LOGO_URL, document_root=settings.COMPONENT_LOGO)
