"""babysecurity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import (handler400, handler403, handler404, handler500)
from django.conf.urls.static import static
from . import settings

handler404 = 'errorpage.views.pageNotFoundPage'
handler500 = 'errorpage.views.serverErrorPage'
handler403 = ''
handler400 = 'errorpage.views.badRequestPage'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'parent/', include("parent.urls")),
    path(r'rasberrypy/', include('rasberrypy.urls')),
    path(r'account/',include('account.urls')),
]

urlpatterns += static("media",document_root=settings.MEDIA_ROOT)
