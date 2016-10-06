from django.contrib.auth.models import User
from django.db import models as m
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.core.files.storage import FileSystemStorage


def media_location(instance, filename):
    return '{}/{}'.format(instance.id, filename)


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
    media = m.FileField(blank=True, null=True, upload_to=media_location)
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


# this can be used to manipulate data before saving it to DB!
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_unique_slug(instance)
        print('Added slug {} to instance {}'.format(instance.slug, instance))

pre_save.connect(product_pre_save_receiver, sender=Product)


# This could be use to notify other parts of the app when a new item has been added to DB
def product_post_save_receiver(sender, instance, *args, **kwargs):
    print('Product has been saved with ID {}'.format(instance.id))


post_save.connect(product_post_save_receiver, sender=Product)

# There are also actions available for delete and init
