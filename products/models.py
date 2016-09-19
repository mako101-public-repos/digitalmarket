from django.db import models as m

# Create your models here.

class Product(m.Model):
    title = m.CharField(max_length=30)
    description = m.TextField()
    price = m.DecimalField(max_digits=100, decimal_places=2, default=9.99)
    sale_price = m.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)
    is_available = m.BooleanField(default=True)  # is the product available to purchase?

    def __str__(self):
        return self.title
