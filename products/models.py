from django.contrib.auth.models import User
from django.db import models as m
from django.db.models.signals import pre_save, post_save

from django.core.urlresolvers import reverse

# imports for generating thumbnails
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse

# Various functions to make life easier
from . import model_helpers as helpers

THUMBNAIL_CHOICES = (
    ('hd', 'HD'),
    ('sd', 'SD'),
    ('micro', 'Micro')
)

############################ Model Classes ##########################
class Product(m.Model):

    # One-to-one mapping example
    # owner = m.OneToOneField(User)

    # Many-to-one mapping
    owner = m.ForeignKey(User, related_name='product_owner')
    # Many-to-many mapping
    managers = m.ManyToManyField(User, related_name='product_managers', blank=True)

    title = m.CharField(max_length=30)
    slug = m.SlugField(blank=True, unique=True)
    description = m.TextField(blank=True)
    media = m.ImageField(blank=True, null=True, upload_to=helpers.media_location)
    price = m.DecimalField(max_digits=100, decimal_places=2, default=9.99)
    sale_price = m.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)
    on_sale = m.BooleanField(default=False)
    is_available = m.BooleanField(default=True)  # is the product available to purchase?

    def __str__(self):
        return self.title

    # the URL to redirect to upon successful creation of the model instance
    # This will be used for both create and edit views unless overwritten
    def get_absolute_url(self):
        view_name = 'products:detail_slug'
        print('The absolute URL is:', reverse(view_name, kwargs={'slug': self.slug}))
        return reverse(view_name, kwargs={'slug': self.slug})

    #  This will provide a download link for the product
    def get_download(self):
        view_name = 'products:download'
        url = reverse(view_name, kwargs={'pk': self.id})
        return url

    @property
    def get_price(self):
        if self.sale_price and self.on_sale:
            return self.sale_price
        return self.price


class Thumbnail(m.Model):
    product = m.ForeignKey(Product)
    # user = m.ForeignKey(User)
    type = m.CharField(max_length=20, choices=THUMBNAIL_CHOICES, default='hd')
    height = m.CharField(max_length=20, null=True, blank=True)
    width = m.CharField(max_length=20, null=True, blank=True)
    media = m.ImageField(
        height_field='height', width_field='width',
        blank=True, null=True, upload_to=helpers.thumbnail_location)

    def __str__(self):
        # This effectively returns product slug + thumbnail filename
        return self.media.name


class MyProducts(m.Model):
    user = m.OneToOneField(User)
    products = m.ManyToManyField(Product, blank=True)

    def __str__(self):
        # Get titles of all products the user owns
        product_titles = [product.title for product in self.products.all()]

        # Make a string out of them
        product_list = product_titles[0]
        for product in product_titles[1:]:
            product_list = product_list + ', ' + product
        product_set = '{} - {}'.format(str(self.user).capitalize(), product_list)
        return product_set

    # This allows to change the names used in Admin section :)
    class Meta:
        verbose_name = 'My Products'
        verbose_name_plural = 'My Products'


###################################### Signal Functions ######################################
# this can be used to manipulate data before saving it to DB!
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = helpers.create_unique_slug(Product, instance)
        print('Added slug {} to instance {}'.format(instance.slug, instance))

pre_save.connect(product_pre_save_receiver, sender=Product)


# This could be use to notify other parts of the app when a new item has been added to DB
def product_post_save_receiver(sender, instance, created, *args, **kwargs):
    print('Product has been saved with ID {}'.format(instance.id))

    if instance.media:
        try:
            # .get_or_create method returns a tuple
            # 1st item is an object itself
            # 2nd is boolean, true if just created, false if already existed
            hd, hd_created = Thumbnail.objects.get_or_create(product=instance, type='hd')
            sd, sd_created = Thumbnail.objects.get_or_create(product=instance, type='sd')
            micro, micro_created = Thumbnail.objects.get_or_create(product=instance, type='micro')

            media_path = instance.media.name
            owner_slug = instance.slug

            if hd_created:
                helpers.create_thumbnail(media_path, hd, owner_slug, 'hd')

            if sd_created:
                helpers.create_thumbnail(media_path, sd, owner_slug, 'sd')

            if micro_created:
                helpers.create_thumbnail(media_path, micro, owner_slug, 'micro')

        # This DOES NOT work! It just saves multiples and continues  :-/
        # but at least it doesnt crash
        except MultipleObjectsReturned:
            print('ERROR detected')
            return HttpResponse('You can only have one of each type of thumbnail', status=403)

post_save.connect(product_post_save_receiver, sender=Product)
# There are also actions available for delete and init