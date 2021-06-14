from django.conf.urls import url
from . import views

urlpatterns  = [
    url(r'^$', views.index, name="internships"),
    url(r'^internshipData/',views.internshipData,name='internshipData'),
    url(r'^uploadIndustryData/',views.uploadIndustryData,name='uploadIndustryData'),
    url(r'^applyInternship$', views.applyInternship, name="applyInternship"),
    url(r'^industrialVisits', views.industrialVisitData, name='industrialVisits'),
    url(r'^applications/(?P<indId>[0-9]+)', views.intApplications, name="intApplications"),
    url(r'^confirm/', views.confirmInternship, name="confirmInternship"),

    url(r'^RecomandUsers/', views.RecomandUsers, name="RecomandUsers"),
    url(r'^applyIV/(?P<IVId>[0-9]+)', views.applyIV, name="applyIV"),
    url(r'^CreatingGroup/(?P<IVId>[0-9]+)', views.CreatingGroup, name="CreatingGroup"),
    url(r'^listOfApplicants/(?P<IVId>[0-9]+)', views.listOfApplicants, name="listOfApplicants"),
    url(r'^confirmIV/', views.confirmIV, name="confirmIV"),
    url(r'^cancleGroup/', views.cancleGroup, name="cancleGroup"),
    url(r'^notificationData/', views.notificationData, name="notificationData"),
    url(r'^notify/', views.notify, name="notify"),
    url(r'^notificationResp/', views.notificationResp, name="notificationResp"),

    url(r'^DoneIV/', views.DoneIv, name="DoneIv"),
    url(r'^listOfMembers/(?P<IVId>[0-9]+)', views.listOfMembers, name="listOfApplicants"),

    url(r'^getIvs$', views.getIVs, name="getIvs"),
]
