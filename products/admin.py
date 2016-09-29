from django.contrib import admin

# Register your models here.
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'id', 'description', 'owner',
                    'price', 'sale_price', 'is_available']  # fields that are visible in the Product Admin

    # to search for foreign keys, you have to use [model_field__foreign_key_field] notation
    # i.e owner__username to look up owner of the product
    # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
    search_fields = ['title', 'description', 'owner__username', 'id']  # what can we search by

    list_filter = ['price', 'sale_price', 'owner', 'is_available']  # for the filter option on the right
    list_editable = ['sale_price', 'is_available']  # which fields we can edit right from the admin page!

    class Meta:
        model = Product

# admin.site.register(Product, ProductAdmin) # @admin.register(Product) does the same
