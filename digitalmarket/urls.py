from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from dashboard.views import DashboardView


urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^admin/', admin.site.urls),
    # url(r'^$', RedirectView.as_view(url='products/')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^tags/', include('tags.urls', namespace='tags')),


    ####################### Old function-based views, for reference #################################
    # url(r'^list/$', product_views.list_view, name='list_view'),
    # url(r'^create/$', product_views.create_view, name='create_view'),
    # url(r'^detail/(?P<object_id>\d+)/$', product_views.detail_view, name='detail_view'),
    # url(r'^detail/(?P<object_id>\d+)/edit/$', product_views.update_view, name='update_view'),
    # url(r'^detail/(?P<slug>[\w-]+)/$', product_views.detail_slug_view, name='detail_slug_view'),
    # url(r'^detail/$', product_views.detail_view, name='detail_view')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL)
