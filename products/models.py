from django.contrib.auth.models import User
from django.db import models as m
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse

# imports for generating thumbnails
import os
import shutil
import random
from PIL import Image
from django.core.files import File


##################################  Helper Functions ###########################################
THUMBNAIL_CHOICES = (
    ('hd', 'HD'),
    ('sd', 'SD'),
    ('micro', 'Micro')
)


def media_location(instance, filename):
    return '{}/{}'.format(instance.slug, filename)


def thumbnail_location(instance, filename):
    return '{}/{}-thumbnail'.format(instance.product.slug, filename)


def create_unique_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    slug_exists = Product.objects.filter(slug=slug).exists()

    if slug_exists:
        # Split slug on dashes and check if the last part is a digit
        split_slug = slug.split('-')
        last = split_slug[-1]

        if last.isdigit():
            # If yes, we will increment the number and update the slug with it
            last_index = (split_slug.index(last))
            split_slug[last_index] = int(last) + 1
            split_slug = [str(i) for i in split_slug]
            new_slug = '-'.join(split_slug)
        else:
            # If not, we just add '-1' at the end of the slug
            # it can be incremented if another product with the same title is added :)
            new_slug = "{}-{}".format(slug, 1)

        # Rerun the function with the new slug
        slug = create_unique_slug(instance, new_slug)
    return slug


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
    media = m.ImageField(blank=True, null=True, upload_to=media_location)
    price = m.DecimalField(max_digits=100, decimal_places=2, default=9.99)
    sale_price = m.DecimalField(max_digits=100, decimal_places=2, default=6.99, null=True, blank=True)
    is_available = m.BooleanField()  # is the product available to purchase?

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


class Thumbnail(m.Model):
    product = m.ForeignKey(Product)
    # user = m.ForeignKey(User)
    type = m.CharField(max_length=20, choices=THUMBNAIL_CHOICES, default='hd')
    height = m.CharField(max_length=20, null=True, blank=True)
    width = m.CharField(max_length=20, null=True, blank=True)
    media = m.ImageField(
        height_field='height', width_field='width',
        blank=True, null=True, upload_to=thumbnail_location)

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
        instance.slug = create_unique_slug(instance)
        print('Added slug {} to instance {}'.format(instance.slug, instance))

pre_save.connect(product_pre_save_receiver, sender=Product)

# need to have a local copy of the uploaded image for this to work!!

def create_thumbnail(media_path, instance, owner_slug, size):

    max_sizes = {
        'hd': (400, 500),
        'sd': (200, 300),
        'micro': (100, 150)
        }

    filename = '{}-{}'.format(os.path.basename(media_path), size)
    print(filename)
    dimensions = max_sizes[size]
    print(dimensions)
    thumb = Image.open(media_path)
    thumb.thumbnail(dimensions, Image.ANTIALIAS)

    temp_location = os.path.join('tmp', 'products', owner_slug)
    print(temp_location)
    if not os.path.exists(temp_location):
        os.makedirs(temp_location)
    temp_file_path = os.path.join(temp_location, filename)

    temp_image = open(temp_file_path, 'wb')
    thumb.save(temp_image)

    temp_image = open(temp_file_path, 'rb')
    thumb_file = File(temp_image)
    instance.media.save(filename, thumb_file)

    # Delete all temp stuff
    # shutil.rmtree(temp_location, ignore_errors=True)


# This could be use to notify other parts of the app when a new item has been added to DB
def product_post_save_receiver(sender, instance, created, *args, **kwargs):
    print('Product has been saved with ID {}'.format(instance.id))

    if instance.media:
        hd, hd_created = Thumbnail.objects.get_or_create(product=instance, type='hd')
        # sd = Thumbnail.objects.get_or_create(product=instance, type='sd')
        # micro = Thumbnail.objects.get_or_create(product=instance, type='micro')

        media_path = instance.media.name
        owner_slug = instance.slug

        if hd_created:
            create_thumbnail(media_path, hd, owner_slug, 'hd')






post_save.connect(product_post_save_receiver, sender=Product)
# There are also actions available for delete and init