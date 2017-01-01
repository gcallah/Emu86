from django.conf.urls import url

from . import views

app_name = 'Emu86'


urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^help/*$', views.help, name='help'),
    url(r'^feedback/*$', views.feedback, name='feedback'),
]
