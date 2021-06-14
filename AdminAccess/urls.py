from django.conf.urls import url
from . import views

app_name = 'AdminAccess'
urlpatterns = [
    url(r'^$', views.index_admin, name='index_admin'),
    url(r'^saveQuotes/$', views.saveQuotes, name='saveQuotes'),
    url(r'^deletePaper/$', views.deletePaper, name='deletePaper'),
]
