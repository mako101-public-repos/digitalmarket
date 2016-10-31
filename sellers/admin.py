from django.contrib import admin
from sellers.models import SellerAccount


# Register your models here.
@admin.register(SellerAccount)
class SellerAccountAdmin(admin.ModelAdmin):

    list_display = ['user', 'active']
    list_editable = ['active']

    class Meta:
        model = SellerAccount
