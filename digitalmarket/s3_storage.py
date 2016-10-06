from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# We have to overwrite storage class to allow using different subdirs for media and static
class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
