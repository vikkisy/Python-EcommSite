# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 02:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_auto_20170927_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity_purchased',
            field=models.IntegerField(null=True),
        ),
    ]
