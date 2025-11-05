from django.urls import path

from . import views

app_name = 'Emu86'


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('main/', views.main_page, name='main_page'),
    path('help/', views.help, name='help'),
    path('feedback/', views.feedback, name='feedback'),
    path("emu/<slug:slug>/", views.main_page, name="emu_page"),

]
