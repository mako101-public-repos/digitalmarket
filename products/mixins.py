from django.http import Http404
from digitalmarket.mixins import LoginRequiredMixin

# These are product-specific mixins so we store them in a separate file


class ProductManagerEditMixin(LoginRequiredMixin, object):

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
            raise Http404('You are not authorised to edit this product!')


class ProductManagerDetailMixin(LoginRequiredMixin, object):

    def get_context_data(self, **kwargs):
        context = super(ProductManagerDetailMixin, self).get_context_data()
        user = self.request.user
        obj = super(ProductManagerDetailMixin, self).get_object()
        if obj.owner == user or user in obj.managers.all():
            context['allowed_to_edit'] = True

        print('Using detail CBV!\n')
        print(context)
        return context



