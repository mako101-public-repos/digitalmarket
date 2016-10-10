# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-03 19:13
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20160929_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to=products.models.media_location),
        ),
    ]