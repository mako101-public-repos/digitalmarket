from django.contrib import admin

# Register your models here.
from .models import *


# inlines allow for editing related models on the same page as a parent model
# can be TabularInline (horizontal) or StackedInline (vertical)
# https://docs.djangoproject.com/en/1.10/ref/contrib/admin/#django.contrib.admin.TabularInline
class ThumbnailInline(admin.TabularInline):
    # amount of lines for filling
    extra = 0
    model = Thumbnail


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ThumbnailInline]
    # the first item is what the product list is ordered by
    list_display = ['slug', '__str__', 'id', 'description', 'owner',
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

admin.site.register(MyProducts)
admin.site.register(Thumbnail)
