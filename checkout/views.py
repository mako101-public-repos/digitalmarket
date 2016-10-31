from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import View

from products.models import Product, MyProducts
from billing.models import Transaction
from digitalmarket.mixins import AjaxRequiredMixin


# Create your views here.
class CheckoutAjaxView(AjaxRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        # This does nothing, as CSRF token is not passed for unauthed users!
        if not request.user.is_authenticated():
                return JsonResponse({}, status=401)
        user = request.user
        product_id = request.POST.get('product_id')
        print('Product ID is: {}'.format(product_id))
        # Verify that the product being purchased is still there!
        product_exists = Product.objects.filter(id=product_id).exists()
        if not product_exists:
            return JsonResponse({}, status=404)

        try:
            purchased_product = Product.objects.get(id=product_id)
        except:
            purchased_product = Product.objects.filter(id=product_id).first()

        # Run transaction, assume its successful by default
        transaction = Transaction.objects.create(
            user=user,
            product=purchased_product,
            price=purchased_product.get_price
        )

        # Retrieve or create the list of products owned by user
        # and add the newly purchased product to it
        try:
            my_products = MyProducts.objects.get_or_create(user=request.user)[0]
            my_products.products.add(purchased_product)

            download_link = purchased_product.get_download()
            preview_link = download_link + '?preview=True'
            data = {
                'time': datetime.now(),
                'download': download_link,
                'preview': preview_link
            }
            return JsonResponse(data)

        except:
            return JsonResponse({}, status=500)


class CheckoutTestView(View):

    def post(self, request, *args, **kwargs):
        request_data = request.POST.get('testData')

        print(request_data)
        if request.is_ajax():

            # This does nothing!
            if not request.user.is_authenticated():
                data = {
                    'works': False
                }
                return JsonResponse(data, status=401)
            data = {
                'works': True,
                'time': datetime.now()
            }
            return JsonResponse(data)

        return HttpResponse(request_data)
