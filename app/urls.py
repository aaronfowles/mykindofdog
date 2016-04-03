from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_dogs', views.get_dogs, name='get_dogs'),
    url(r'^record_selection', views.record_selection, name='record_selection'),
    url(r'^database', views.database, name='database'),
]

urlpatterns += staticfiles_urlpatterns()
