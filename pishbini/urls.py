"""pishbini URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from pishi import views as core_views
from pishi.registrar import urls as registrar_urls
from pishi.match import urls as match_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', core_views.index),
    url(r'^home/$', core_views.home, name='home'),
]

urlpatterns.extend(registrar_urls.urlpatterns)
urlpatterns.extend(match_urls.urlpatterns)
