from django.conf.urls import url
from django.contrib import admin
from sellers.views import *

urlpatterns = [

    url(r'^$', SellerDashboard.as_view(), name='dashboard'),
    url(r'^transactions/', SellerTransactionList.as_view(), name='transactions')
]