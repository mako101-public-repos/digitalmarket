from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.TagListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', views.TagDetailView.as_view(), name='detail'),
]