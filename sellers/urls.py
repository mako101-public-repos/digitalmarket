from django.conf.urls import url
from sellers import views as s_views
from products import views as p_views

urlpatterns = [

    url(r'^$', s_views.SellerDashboard.as_view(), name='dashboard'),
    url(r'^products/$', p_views.SellerProductListView.as_view(), name='product_list'),
    url(r'^products/add/$', p_views.ProductCreateView.as_view(), name='product_add'),
    url(r'^products/(?P<pk>\d+)/$', s_views.SellerProductDetailRedirectView.as_view()),
    url(r'^products/(?P<pk>\d+)/edit/$', p_views.ProductEditView.as_view(), name='product_edit'),
    url(r'^transactions/', s_views.SellerTransactionList.as_view(), name='transactions')
]