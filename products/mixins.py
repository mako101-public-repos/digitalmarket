from django.http import HttpResponse
from digitalmarket.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.exceptions import ValidationError

from products.models import Product
from tags.models import Tag


# These are product-specific mixins so we store them in a separate file
class ProductManagerEditMixin(LoginRequiredMixin):

    # We import the LoginRequiredMixin here to do multiple checks at once!
    # a) user is authenticated
    # b) user is owner
    # c) user is one of the product managers

    def get_object(self, *args, **kwargs):
        user = self.request.user
        obj = super(ProductManagerEditMixin, self).get_object(*args, **kwargs)
        if obj.owner == user or user in obj.managers.all():
            return obj
        else:
            raise HttpResponse('You are not authorised to edit this product!', status=403)


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


class SimpleSearchMixin(object):
    # Implement simple search
    def get_queryset(self, *args, **kwargs):
        qs = super(SimpleSearchMixin, self).get_queryset(**kwargs)
        print(qs)
        print(self.request.GET)

        # this will look for '?q=<search pattern>
        #  and match it with titles or descriptions
        # '|' is 'OR'; '&' is 'AND'

        # type of search
        title_desc = self.request.GET.get('td')
        price_from = self.request.GET.get('pf')
        price_to = self.request.GET.get('pt')

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
