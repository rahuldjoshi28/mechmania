from django.conf.urls import url
from . import views

urlpatterns=[
url(r'^$', views.projects, name="projects"),
    url(r'^(?P<page>[0-9]+)/', views.projects, name="projects"),
    url(r'^RecomandUsers/', views.RecomandUsers, name="RecomandUsers"),
    url(r'^CreatingGroup/(?P<projectId>[0-9]+)', views.CreatingGroup, name="CreatingGroup"),
    #url(r'^notificationData/', views.notificationData, name="notificationData"),
    #url(r'^notify/', views.notify, name="notify"),
    url(r'^notificationResp/', views.notificationResp, name="notificationResp"),
    url(r'^apply/(?P<projectId>[0-9]+)', views.apply, name="apply"),
    url(r'^listOfApplicants/(?P<projectId>[0-9]+)', views.listOfApplicants, name="listOfApplicants"),
    url(r'^confirm/', views.confirm, name="confirmIV"),
    url(r'^cancleGroup/', views.cancleGroup, name="cancleGroup"),
    url(r'^closeProject/', views.closeProject, name="closeProject"),
    url(r'^groupInfo/(?P<projectId>[0-9]+)', views.groupInfo, name="groupInfo")
]