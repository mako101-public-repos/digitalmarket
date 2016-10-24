from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import View

from products.models import Product, MyProducts

# Create your views here.
class CheckoutAjaxView(View):

    def post(self, request, *args, **kwargs):

        if request.is_ajax():

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

            # Retrieve or create the list of products owned by user
            # and add the newly purchased prodcts to it
            try:
                my_products = MyProducts.objects.get_or_create(user=request.user)[0]
                my_products.products.add(purchased_product)
            except:
                return JsonResponse({}, status=500)
            data = {
                'order_received': True,
                'time': datetime.now()
            }
            return JsonResponse(data)

        raise Http404


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
