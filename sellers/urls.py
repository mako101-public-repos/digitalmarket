from django.conf.urls import url
from django.contrib import admin
from sellers import views

urlpatterns = [

    url(r'^$', views.SellerDashboard.as_view(), name='dashboard')
]