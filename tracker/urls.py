from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<uuid>[^/]+)$', views.track, name='track'),
 	url(r'^mail/new/?$', views.new_mail, name='track'),   
]
