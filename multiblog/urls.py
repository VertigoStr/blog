from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.main, name='main'),
	url(r'^my_profile/(?P<pk>[0-9]+)/$', views.my_profile, name='my_profile'),
	url(r'^new', views.new_publication, name='new'),
	url(r'^publication/(?P<pk>[0-9]+)/$', views.full_publication, name='full'),
	url(r'^publication/(?P<pk>[0-9]+)/edit/$', views.edit_publication, name='edit'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
]