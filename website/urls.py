"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url,include
from django.contrib import admin
from .settings import MEDIA_ROOT,STATIC_ROOT
from django.views.static import serve
# from energy import urls
from django.conf.urls.static import static
urlpatterns = [
    # url(r'^',include('energy.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^energy/', include('energy.urls')),
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

    url(r'^static/(?P<path>.*)', serve, {"document_root":STATIC_ROOT }),

]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

