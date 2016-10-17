from django.db import models as m
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse

from products.models import Product

from django.db.models.query import QuerySet

## this we can se with products
# class CarManager(m.Manager):
#     def get_queryset(self):
#         return super(CarManager, self).get_queryset().filter()


class ActiveTagManager(m.Manager):
    def get_queryset(self):
        return super(ActiveTagManager, self).get_queryset().filter(active=True).order_by('title')


class Tag(m.Model):
    title = m.CharField(max_length=120, unique=True)
    slug = m.SlugField(blank=True, unique=True)
    products = m.ManyToManyField(Product, blank=True)
    active = m.BooleanField(default=True)

    # This will allow us to use Tags.active_tags.all() etc type of queries :)
    active_tags = ActiveTagManager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        view_name = 'tags:detail'
        # print('The absolute URL is:', reverse(view_name, kwargs={'slug': self.slug}))
        return reverse(view_name, kwargs={'slug': self.slug})


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(tag_pre_save_receiver, sender=Tag)

