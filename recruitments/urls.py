from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^search$', views.search, name="search"),
    url(r'^apply$', views.applyRec, name="apply"),
    url(r"confirm$", views.confirmRec, name="confirm"),

    #this is page where requests are shown to admin
    url(r'^adminConfirm/', views.adminConfirm, name="adminConfirm"),

    # actual function when admin clicks confirm
    url(r'^confirm', views.confirmRec, name="confirm"),

    #get recruitment for single industry
    url(r'^getrec$', views.getRecruitments, name="getrecruitments"),
]