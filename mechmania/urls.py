"""mechmania URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url,include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.staticfiles.views import serve as serve_static
from django.views.decorators.cache import never_cache

handler404 = 'mechmania.views.not_found'
handler500 = 'mechmania.views.server_error'
handler403 = 'mechmania.views.permission_denied'
handler400 = 'mechmania.views.bad_request'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^contactus/', views.contact_us, name='contactus'),
    url(r'^aboutus/', views.aboutus, name='aboutus'),
    url(r'^', include('Accounts.urls_django_auth')),
    url(r'^', include('Accounts.urls')),
    url(r'^questionPapers/', include('questionPapers.urls')),
    url(r'^internships/', include('internships.urls')),
    url(r'^recruitments/',include('recruitments.urls')),

    url(r'^notifications/$', views.notifications, name='notifications'),

    url(r'^shortNotifications/', include('notifications.urls')),

    url(r'^industry/(?P<industryName>[\w.@+-]+)/$', views.industry, name='industry'),
    url(r'^internshipsandvisits/$', views.internshipsandvisits, name='internshipsandvisits'),
    url(r'^adminaccess/', include('AdminAccess.urls')),
    url(r'^questionPapers/', include('questionPapers.urls')),

    url(r'^recruitments/', include('recruitments.urls')),

    url(r'^search/', views.search, name="search"),

    url(r'^projects/', include('project.urls')),
]
