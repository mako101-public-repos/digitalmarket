from django.contrib import admin


# Register your models here.
from billing.models import Transaction

admin.site.register(Transaction)
