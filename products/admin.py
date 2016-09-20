from django.contrib import admin

# Register your models here.
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'description', 'price', 'sale_price', 'is_available']  # fields that are visible in the Product Admin
    search_fields = ['title', 'description', 'is_available']  # what can we search by
    list_filter = ['price', 'sale_price', 'is_available']  # for the filter option on the right
    list_editable = ['sale_price', 'is_available']  # which fields we can edit right from the admin page!

    class Meta:
        model = Product

# admin.site.register(Product, ProductAdmin) # @admin.register(Product) does the same
