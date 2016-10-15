# imports for generating thumbnails
import os
import shutil
from PIL import Image
from django.core.files import File
from digitalmarket import settings
import requests
from io import BytesIO

from django.utils.text import slugify


def media_location(instance, filename):
    return '{}/{}'.format(instance.slug, filename)


def thumbnail_location(instance, filename):
    return '{}/{}'.format(instance.product.slug, filename)


def create_unique_slug(parent_class, instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    # slug_exists = Product.objects.filter(slug=slug).exists()
    slug_exists = parent_class.objects.filter(slug=slug).exists()

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
        slug = create_unique_slug(parent_class, instance, new_slug)
    return slug


def create_thumbnail(media_path, instance, owner_slug, size):

    max_sizes = {
        # width, height
        'hd': (600, 500),
        'sd': (400, 300),
        'micro': (200, 150)
        }

    # Disassemble filename to add size to the name
    media_name = os.path.basename(media_path)
    base_name = os.path.splitext(media_name)[0]
    ext = os.path.splitext(media_name)[1].lower()
    # get rid of the dot in the extension
    ext = ext[1:]
    # e.g 'batman-thumb-hd.png'
    filename = '{}-{}-{}.{}'.format(base_name, 'thumb', size, ext)
    print('Thumbnail\'s filename:', filename)

    # get the original image from AWS for processing
    dimensions = max_sizes[size]
    print('Thumbnail\'s dimensions:', dimensions)
    image_url = settings.MEDIA_URL + media_path
    image_data = requests.get(image_url)
    print('AWS Image URL:', image_url)
    thumb = Image.open(BytesIO(image_data.content))
    thumb.thumbnail(dimensions, Image.ANTIALIAS)

    temp_location = os.path.join('/tmp', 'products', owner_slug)
    print(temp_location)
    if not os.path.exists(temp_location):
        os.makedirs(temp_location)
    temp_file_path = os.path.join(temp_location, filename)
    print('Temporary filepath:', temp_file_path)

    temp_image = open(temp_file_path, 'wb')
    thumb.save(temp_image, format='png')

    temp_image = open(temp_file_path, 'rb')
    thumb_file = File(temp_image)
    instance.media.save(filename, thumb_file)

    # Delete all temp stuff
    shutil.rmtree(temp_location, ignore_errors=True)