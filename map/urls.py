from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.map_disp, name='map_disp'),
    url(r'^staticImage.png$', views.showStaticImage, name='map_disp'),
]
