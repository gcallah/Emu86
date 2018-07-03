from django.conf.urls import url

from . import views

app_name = 'Emu86'


urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^main/*$', views.main_page, name='main_page'),
    url(r'^help/*$', views.help, name='help'),
    url(r'^feedback/*$', views.feedback, name='feedback'),
]
