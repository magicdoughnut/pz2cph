from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /maps/
    url(r'^$', views.stats, name='stats'),
    ]