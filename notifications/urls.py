from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.return_messages, name="notifications"),
    url(r'^delete_notice/', views.delete_notice, name="delete_notice"),
]