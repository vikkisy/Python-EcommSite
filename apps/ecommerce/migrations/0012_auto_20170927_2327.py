# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-28 06:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0011_auto_20170927_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='ecommerce.Cart'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='items',
            field=models.ManyToManyField(null=True, related_name='items', to='ecommerce.Item'),
        ),
    ]