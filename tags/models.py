from django.db import models as m
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet

from products.models import Product


class ActiveTagManager(m.Manager):
    def get_queryset(self):
        return super(ActiveTagManager, self).get_queryset().filter(active=True).order_by('title')


# this is redundant, but just for illustration
# how to make a dynamic queryset
# Tag.objects.all().active()
class ActiveTagQuerySet(QuerySet):
    def active(self):
        return self.filter(active=True)


class TagManager(m.Manager):
    def get_queryset(self):
        return ActiveTagQuerySet(self.model, using=self.db)

    # the point of this whole exercise is that it lets us apply .active() filter! :-/
    def all(self, *args, **kwargs):
        return super(TagManager, self).all(*args, **kwargs).active()


class Tag(m.Model):
    title = m.CharField(max_length=120, unique=True)
    slug = m.SlugField(blank=True, unique=True)
    products = m.ManyToManyField(Product, blank=True)
    active = m.BooleanField(default=True)

    # We need to explicitly define the default manager or it wont be used
    # It also has to be first to be default!!!
    # https://docs.djangoproject.com/en/1.10/topics/db/managers/#default-managers
    objects = m.Manager()

    # This will allow us to use Tags.active_tags.all() etc type of queries :)
    active_tags = ActiveTagManager()

    tags = TagManager()

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

