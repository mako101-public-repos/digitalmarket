from django.http import HttpResponse, Http404
from digitalmarket.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.exceptions import ValidationError

from products.models import *
from tags.models import Tag

from sellers.mixins import SellerAccountMixin

# Implement simple search
def perform_search(request, qs):
    # this will look for '?q=<search pattern>
    #  and match it with titles or descriptions
    # '|' is 'OR'; '&' is 'AND'

    # type of search
    title_desc = request.GET.get('td')
    price_from = request.GET.get('pf')
    price_to = request.GET.get('pt')

    # Perform search if any of the search parameters are received
    if title_desc or price_from or price_to:
        try:
            # title and description
            if title_desc:
                matching_tags = Tag.active_tags.filter(
                    title__icontains=title_desc)

                qs = qs.filter(
                    Q(title__icontains=title_desc) |
                    Q(description__icontains=title_desc) |
                    Q(tag__in=matching_tags))

            else:
                if price_from and price_to:
                    qs = qs.filter(
                        Q(price__gte=price_from) &
                        Q(price__lte=price_to))

                elif price_from:
                    qs = qs.filter(price__gte=price_from)

                elif price_to:
                    qs = qs.filter(price__lte=price_to)

        except ValidationError:
            qs = qs.filter(Q(title__icontains=title_desc) |
                           Q(description__icontains=title_desc))

        return qs.order_by('title').distinct()

    else:
        # Otherwise return an ordered product list
        print('Full product list')
        return qs.order_by('slug')


# These are product-specific mixins so we store them in a separate file
class ProductManagerEditMixin(SellerAccountMixin, object):

    # We import the LoginRequiredMixin here to do multiple checks at once!
    # a) user is authenticated
    # b) user is owner
    # c) user is one of the product managers

    def get_object(self, *args, **kwargs):
        obj = super(ProductManagerEditMixin, self).get_object(*args, **kwargs)
        user = self.request.user
        seller = self.get_account()
        if str(seller) == str(user):
            return obj
        else:
            raise Http404('You are not authorised to edit this product!')


class ProductManagerDetailMixin(LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = super(ProductManagerDetailMixin, self).get_context_data()
        context['coming_soon'] = Product.objects.get(slug='coming-soon')
        user = self.request.user
        obj = super(ProductManagerDetailMixin, self).get_object()
        # if obj.owner == user or user in obj.managers.all():
        if obj.seller == user:
            context['allowed_to_edit'] = True

        print('Using detail CBV!\n')
        print(context)
        return context


class SearchMixin(object):
    # This will search all products, and can be run by unauthorised user
    def get_queryset(self, **kwargs):
        qs = super(SearchMixin, self).get_queryset(**kwargs)
        qs = perform_search(self.request, qs)
        return qs


class SellerSearchMixin(SellerAccountMixin, object):
    # This will search only products owned by the seller, requires auth
    def get_queryset(self, **kwargs):
        seller = self.get_account()
        qs = super(SellerSearchMixin, self).get_queryset(**kwargs)
        qs = qs.filter(seller=seller)

        qs = perform_search(self.request, qs)
        return qs


class ComingSoonMixin(object):

    # this displays "Coming Soon" image for products that don't have media
    def get_context_data(self, **kwargs):
        context = super(ComingSoonMixin, self).get_context_data()
        print(context)
        context['coming_soon'] = Product.objects.get(slug='coming-soon')
        # context['queryset'] = self.get_queryset()
        return context