from django import template
from products.models import Product, THUMBNAIL_CHOICES

register = template.Library()

# Get the specific thumbnail type for the given Product
@register.filter
def get_thumbnail(product, type):

    type = type.lower()

    # We can build in validation as well :)
    if not isinstance(product, Product):
        raise TypeError('This filter should be used with a Product model instance')

    choices = dict(THUMBNAIL_CHOICES)
    if not choices.get(type):
        raise TypeError('Valid thumbnail types are: {}'.format(choices.keys()))

    return product.thumbnail_set.filter(type=type).first().media.url


