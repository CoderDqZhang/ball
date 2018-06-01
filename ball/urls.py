"""ball URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from ball import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^ball/', include('mycode.urls.urls')),
]
#七牛保存文件路径
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#本地保存文件路径
urlpatterns += static(settings.MEDIA_URL1, document_root=settings.MEDIA_ROOT1)
#静态文件路径
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
