from django.conf.urls import url,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^searchPaper/',views.getPaperList ,name='getPaperList'),
    url(r'^uploadsuccess/',views.uploadsuccess,name='uploadsuccess'),
    url(r'^show/',views.getFile,name="show"),
    #url(r'(?P<paper_id>[0-9]+)/show/$',views.getFile,name="show"),
]
"""
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)"""
