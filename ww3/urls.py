from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /maps/
    url(r'^$', views.index, name='index'),
    # ex: /map/5042/
    #url(r'^(?P<latlon>[0-9]+)/$', views.map_disp, name='map_disp'),
    url(r'^(?P<latlon>.+)/$', views.map_disp, name='map_disp'),
    #url(r'^result.png$', views.plotResults, name='map_disp'),
    url(r'^result.png$', views.plotResults, name='plotResults'),
    ]