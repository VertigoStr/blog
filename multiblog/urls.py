from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.MainPageAuth.as_view(), name='main'),
	url(r'^my_profile/(?P<pk>[0-9]+)/$', views.MyProfile.as_view(), name='my_profile'),
	url(r'^new', views.NewPublication.as_view(), name='new'),
	url(r'^publication/(?P<pk>[0-9]+)/$', views.FullPublication.as_view(), name='full'),
	url(r'^publication/(?P<pk>[0-9]+)/edit/$', views.EditPublication.as_view(), name='edit'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	url(r'^delete/$', views.delete, name='delete'),
	url(r'^edit/(?P<pk>[0-9]+)/$', views.edit, name='edit_profile'),
	url(r'^search/$', views.search, name='search'),
	url(r'^rating/$', views.rating, name='rating'),
]