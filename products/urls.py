from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.ProductListView.as_view(), name='list'),
    url(r'^add/$', views.ProductCreateView.as_view(), name='add'),

    url(r'^(?P<pk>\d+)/edit/$', views.ProductEditView.as_view(), name='edit'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.ProductEditView.as_view(), name='edit_slug'),

    url(r'^(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name='detail'),
    # the slug url should be below the PK one, to avoid not found errors
    # because the slug regex will match the PK as well
    url(r'^(?P<slug>[\w-]+)/$', views.ProductDetailView.as_view(), name='detail_slug'),

    url(r'^(?P<pk>\d+)/download/', views.ProductDownloadView.as_view(), name='download'),
    url(r'^(?P<slug>[\w-]+)/download/', views.ProductDownloadView.as_view(), name='download_slug'),
]
