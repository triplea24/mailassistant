"""mailasist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, authtoken
from tracker import views
from panel import views as panelviews
from rest_framework.authtoken import views as authviews
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views_html

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'mails',views.MailViewSet,base_name='sender')
router.register(r'log',views.LogViewSet,base_name='log')
# router.register(r'mails',view.Ma)

urlpatterns = [
	url(r'^api/', include(router.urls)),
	url(r'^api-token-auth/', authviews.obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^track/', include('tracker.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^',include('panel.urls')),
    url(r'^logout/$', auth_views_html.logout,{'next_page': '/register/'}, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)