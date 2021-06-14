from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'Accounts'
urlpatterns = [
    url(r'^profile/',views.profile, name='profile'),
    url(r'^username/(?P<username>[\w.@+-]+)/$',views.usernameProfile, name='usernameProfile'),
    url(r'^change_profile_picture/',views.change_profile_picture, name='change_profile_picture'),
    url(r'^updateProfile/',views.updateProfile, name='updateProfile'),
    url(r'^login.html',auth_views.login,{'template_name': 'loginsignup.html'}, name='login'),
	url(r'^logout/$',auth_views.logout, name='logout', kwargs={'next_page': '/loginsignup.html'}),
	url(r'^signup.html', views.signup, name='signup'),
    url(r'^loginsignup.html', views.loginsignup, name='loginsignup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^account_activation_invalid/$', views.account_activation_invalid, name='account_activation_invalid'),
]
