from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.main, name='main'),
	url(r'^my_profile/$', views.my_profile, name='my_profile'),
	url(r'^new', views.new_publication, name='new'),
]