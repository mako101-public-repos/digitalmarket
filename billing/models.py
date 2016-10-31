from django.db import models as m
from django.contrib.auth.models import User
from products.models import Product


# Create your models here.
class Transaction(m.Model):

    user = m.ForeignKey(User)
    product = m.ForeignKey(Product)
    price = m.DecimalField(max_digits=100, decimal_places=2)
    timestamp = m.DateTimeField(auto_now_add=True, auto_now=False)
    success = m.BooleanField(default=True)

    # To be added later
    # transaction_id_payment_system = Braintree / Stripe
    # payment_method
    # last_four (digits of the credit card)

    def __str__(self):
        return '{}----{}----{}--{}--{}'.format(self.id, self.timestamp, self.user, self.product, self.product.get_price)
