from django.conf.urls import url
from sellers import views as s_views
from products import views as p_views

urlpatterns = [

    url(r'^$', s_views.SellerDashboard.as_view(), name='dashboard'),
    url(r'^products/add/$', p_views.ProductCreateView.as_view(), name='add'),
    url(r'^transactions/', s_views.SellerTransactionList.as_view(), name='transactions')
]