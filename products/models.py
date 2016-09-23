from django.db import models as m
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify


# Create your models here.
class Product(m.Model):
    title = m.CharField(max_length=30)
    slug = m.SlugField(blank=True)  # unique=True
    description = m.TextField(blank=True)
    price = m.DecimalField(max_digits=100, decimal_places=2, default=9.99)
    sale_price = m.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)
    is_available = m.BooleanField()  # is the product available to purchase?

    def __str__(self):
        return self.title


# this can be used to manipulate data before saving it to DB!
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
        print('Added slug {} to instance {}'.format(instance.slug, instance))

pre_save.connect(product_pre_save_receiver, sender=Product)


# This could be use to notify other parts of the app when a new item has been added to DB
def product_post_save_receiver(sender, instance, *args, **kwargs):
    print('Product has been saved with ID {}'.format(instance.id))


post_save.connect(product_post_save_receiver, sender=Product)

# There are also actions available for delete and init
