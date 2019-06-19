from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.addUserToDB),
    url(r'^login$', views.loginUserToDB),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
]
