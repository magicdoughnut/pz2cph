from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /maps/
    url(r'^$', views.index, name='index'),
    ]