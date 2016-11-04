from django.shortcuts import render
from django.views.generic import View
import random

from products.models import Product


class DashboardView(View):

    def get(self, request, *args, **kwargs):

        tag_views = None
        products = None
        top_tags = None
        #
        try:
            # get 5 tags most frequented by the given user
            tag_views = request.user.tagview_set.all().order_by('-count')[:5]
        except:
            tag_views = None

        try:
            owned = request.user.myproducts.products.all()
        except:
            owned = None

        print('tag views:', tag_views)
        if tag_views:
            top_tags = [x.tag for x in tag_views]

            # filter all products by tags that the user is interested in
            products = Product.objects.filter(tag__in=top_tags)
            if owned:
                # exclude already owned products from suggestions
                products = products.exclude(pk__in=owned)

            # if we have less than 10 suggestions
            # then pick 10 non-owned products from DB and offer those
            if products.count() < 10:
                # .order_by('?') is returing the queryset in random order
                products = Product.objects.all().order_by('?')
                if owned:
                    # exclude already owned products from suggestions
                    products = products.exclude(pk__in=owned)
                products = products[:10]
            else:
                # .distinct() = unique results :)
                products = products.distinct()
                # offer the products in random order every time
                products = sorted(products, key=lambda x: random.random())
        else:
            products = None
            top_tags = None

        context = {
            'products': products,
            'top_tags': top_tags
        }
        print(context)

        return render(request, 'dashboard/view.html', context)

