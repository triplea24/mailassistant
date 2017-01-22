from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard$', views.panel, name='panel'),
    url(r'^dashboard/show/(?P<track_key>[^/]+)$', views.show, name='show'),
	url(r'^register$', views.register_view, name='register_view'),
	url(r'^login$', views.login, name='login'),
	url(r'^register$', views.register, name='register'),
]