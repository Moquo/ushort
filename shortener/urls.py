from django.urls import path

from . import views

app_name = 'shortener'
urlpatterns = [
    path('', views.index, name='index'),
    path('s/<url_id>', views.redirectUrl, name='redirectUrl')
]