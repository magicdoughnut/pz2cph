from django.conf.urls import url
#from mysite.map.models import map

from . import views

urlpatterns = [
    url(r'^$', views.map_disp, name='map_disp'),
    url(r'^staticImage.png$', 'mysite.map.views.showStaticImage'),
]
